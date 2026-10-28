from pathlib import Path

from horus_intake.client import IntakeSettings
from horus_intake.countries import iso3
from horus_intake.engage import Ledger, acknowledgement_text, derive_code, engagement_name, kickoff_prompt, process, slugify, summarise_run, write_request


def test_country_codes():
    assert iso3("Egypt") == "EGY" and iso3("Arab Republic of Egypt") == "EGY" and iso3("EGY") == "EGY"
    assert iso3("United Kingdom") == "GBR" and iso3("the UK") == "GBR" and iso3("Kingdom of Saudi Arabia") == "SAU" and iso3("KSA") == "SAU"
    assert iso3("Côte d'Ivoire") == "CIV" and iso3("UAE") == "ARE"
    assert iso3("Narnia") is None and iso3("") is None


def test_slug_and_code(tmp_path):
    assert slugify("Ministry of Finance") == "finance"
    assert slugify("The National Telecom Regulatory Authority") == "telecom-regulatory"
    req = {"kind": "engagement", "country": "Egypt", "organisation": "Ministry of Finance", "received_at": "2026-10-27T10:00:00Z"}
    assert derive_code(req, tmp_path) == "EGY-2026-001-finance"
    (tmp_path / "EGY-2026-001-finance").mkdir()
    (tmp_path / "TEST-2026-000").mkdir()  # numbering runs across prefixes: one more than the highest used this year
    assert derive_code(req, tmp_path) == "EGY-2026-002-finance"
    demo = dict(req, kind="demo", preferred_week="10 November")
    assert derive_code(demo, tmp_path) == "DEMO-2026-002-finance"
    assert derive_code(dict(req, country="Narnia"), tmp_path).startswith("INT-2026-")


def test_names_and_texts():
    req = {"kind": "engagement", "name": "Amina Khalil, Director", "email": "a@gov.eg", "organisation": "Ministry of Finance", "country": "Egypt", "scope_text": "SME e-invoicing adoption strategy\nMore detail.", "id": "REQ-1"}
    assert engagement_name(req) == "Ministry of Finance: SME e-invoicing adoption strategy"
    assert engagement_name(dict(req, kind="demo", scope_text="")) == "Demo for Ministry of Finance"
    subject, body = acknowledgement_text(req, "EGY-2026-001-finance")
    assert "EGY-2026-001-finance" in subject and body.startswith("Dear Amina Khalil,") and "technology company" in body
    prompt = kickoff_prompt(req, "EGY-2026-001-finance", None)
    assert "Phase 0" in prompt and "stop there" in prompt and "No acknowledgement" in prompt
    prompt = kickoff_prompt(dict(req, kind="demo", preferred_week="10 November"), "DEMO-2026-001-finance", Path("x"))
    assert "two times in the week of 10 November" in prompt and "acknowledgement-sent.md" in prompt


class FakeClient:
    def __init__(self, requests):
        self.requests = requests
        self.acks = []

    def pending(self):
        return [r for r in self.requests if r["status"] == "new"]

    def download(self, request_id, dest_dir, fallback_name="scope"):
        dest_dir.mkdir(parents=True, exist_ok=True)
        p = dest_dir / "scope.md"
        p.write_bytes(b"# Terms of reference\n")
        return p

    def ack(self, request_id, status="taken", engagement=None, note=None):
        self.acks.append((request_id, status, engagement))
        for r in self.requests:
            if r["id"] == request_id:
                r["status"] = status
        return {}


def test_process_creates_engagement_without_sending_or_starting(tmp_path, monkeypatch):
    monkeypatch.setattr("horus_intake.engage.notify_mac", lambda *a, **k: None)
    monkeypatch.setattr("horus_intake.engage.LOG_FILE", tmp_path / "intake.log")
    req = {"id": "REQ-20261027-ABC123", "kind": "engagement", "status": "new", "received_at": "2026-10-27T10:00:00Z", "name": "Amina Khalil, Director", "email": "a@gov.eg",
           "organisation": "Ministry of Finance", "country": "Egypt", "scope_text": "SME e-invoicing adoption strategy", "attachment": {"name": "scope.md", "size": 21, "type": "text/markdown"}, "page": "https://horushq.ai/"}
    client = FakeClient([req])
    settings = IntakeSettings(site_url="https://example.test", token="t", autostart=False, auto_ack=False, engagements_dir=tmp_path / "engagements")
    ledger = Ledger(tmp_path / "ledger.json")
    result = process(req, client, settings, ledger)
    folder = tmp_path / "engagements" / "EGY-2026-001-finance"
    assert result["code"] == "EGY-2026-001-finance" and Path(result["folder"]) == folder
    assert (folder / ".horus" / "engagement.yaml").exists()
    assert (folder / "inbox" / "request.md").read_text().startswith("# Website request REQ-20261027-ABC123")
    assert (folder / "inbox" / "request.json").exists() and (folder / "inbox" / "scope.md").exists()
    assert client.acks == [("REQ-20261027-ABC123", "taken", "EGY-2026-001-finance")]
    assert not result["acknowledged"] and result["kickoff_log"] is None
    # the same request again is recognised, not re-created
    again = process(req, client, settings, ledger)
    assert again["skipped"] and len(list((tmp_path / "engagements").iterdir())) == 1


def test_write_request_without_file(tmp_path):
    req = {"id": "REQ-1", "kind": "demo", "received_at": "2026-10-27T10:00:00Z", "name": "N", "email": "e@x.org", "organisation": "Org", "country": "", "preferred_week": "", "scope_text": ""}
    write_request(tmp_path, req, None)
    text = (tmp_path / "inbox" / "request.md").read_text()
    assert "demo request" in text and "(none attached)" in text and "(no text; see the document)" in text


def test_summarise_run_reads_result_and_login_state(tmp_path):
    log = tmp_path / "run.jsonl"
    log.write_text('{"type":"system","session_id":"sid-1"}\n{"type":"result","result":"Checkpoint written. Awaiting approval APV-001.","is_error":false,"num_turns":42,"total_cost_usd":1.23,"duration_ms":600000,"session_id":"sid-1"}\n')
    s = summarise_run("EGY-2026-001-finance", "0", log)
    assert s["num_turns"] == 42 and s["cost_usd"] == 1.23 and s["duration_s"] == 600 and not s["not_logged_in"] and s["result"].startswith("Checkpoint")
    assert s["session_id"] == "sid-1"
    log.write_text('{"type":"result","result":"Not logged in · Please run /login","is_error":true}\n')
    assert summarise_run("X", "1", log)["not_logged_in"]


def test_record_acknowledgement_is_sent_under_standing_instruction(tmp_path, monkeypatch):
    from horus_intake import engage
    from horus_state.service import Service

    monkeypatch.setattr("horus_intake.engage.LOG_FILE", tmp_path / "intake.log")
    folder = tmp_path / "EGY-2026-001-test"
    request = {"email": "pm@example.gov", "organisation": "Ministry of Testing", "country": "Egypt", "received_at": "2026-10-28T07:00:00Z", "kind": "engagement", "name": "PM"}
    engage.init_engagement(folder, "EGY-2026-001-test", request)
    body = folder / "inbox" / "acknowledgement-sent.md"
    body.parent.mkdir(exist_ok=True)
    body.write_text("# Acknowledgement sent\n", encoding="utf-8")
    com_id = engage.record_acknowledgement(folder, request, "EGY-2026-001-test", sender="horus@example.com", subject="Horus has received your scope of work", message_id="<x@example.com>", body_path=body)
    assert com_id
    svc = Service(folder, actor="principal")
    com = svc.get("communications", com_id)
    assert com["status"] == "sent" and com["approval"]
    assert svc.get("approvals", com["approval"])["status"] == "approved"
    assert svc.pending_approvals() == []
    assert engage.kickoff_prompt(request, "EGY-2026-001-test", None).startswith("A new scope of work")


def test_run_without_checkpoint_gets_one_continuation(tmp_path, monkeypatch):
    from types import SimpleNamespace

    from horus_intake import engage
    from horus_state.service import Service

    monkeypatch.setattr("horus_intake.engage.LOG_FILE", tmp_path / "intake.log")
    folder = tmp_path / "EGY-2026-001-test"
    engage.init_engagement(folder, "EGY-2026-001-test", {"organisation": "Ministry of Testing", "country": "Egypt"})
    runs = folder / ".horus" / "kickoff"
    runs.mkdir(parents=True)
    (runs / "20260101-000000.jsonl").write_text('{"type":"result","result":"workers still running","is_error":false,"session_id":"sid-9"}\n', encoding="utf-8")
    first = runs / "20260101-000000.jsonl"
    assert engage.latest_session_id(folder) == "sid-9"
    assert engage.needs_continuation("0", {"is_error": False}, first, folder)
    assert not engage.needs_continuation("1", {"is_error": False}, first, folder)
    assert not engage.needs_continuation("0", {"is_error": False}, runs / "20260101-000001-continue.jsonl", folder)

    started = []
    monkeypatch.setattr("horus_intake.engage.subprocess.Popen", lambda *a, **k: started.append(a))
    settings = SimpleNamespace(claude_bin="/usr/bin/true", max_turns=5, allowed_tools=["Read"])
    log_path = engage.kickoff(folder, {}, "EGY-2026-001-test", None, settings, resume="sid-9", prompt=engage.CONTINUE_PROMPT)
    assert log_path and "-continue" in log_path.stem and started
    wrapper = log_path.with_name(log_path.stem + "-run.sh").read_text(encoding="utf-8")
    assert "--resume sid-9" in wrapper
    assert log_path.with_name(log_path.stem + "-prompt.md").read_text(encoding="utf-8") == engage.CONTINUE_PROMPT

    Service(folder, actor="principal").checkpoint(done=["Phase 0 complete"])
    assert not engage.needs_continuation("0", {"is_error": False}, first, folder)
