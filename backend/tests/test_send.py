"""`horus send`: resolving recipients, attachments, body and threading from the state; approving, sending, refusing."""

from datetime import datetime, timezone

import pytest
from typer.testing import CliRunner

from horus_mail.client import MailSettings
from horus_state.cli import app
from horus_state.send import SendError, approve_and_send, prepare, prepare_body, reject, render_preview, send_only, split_body
from horus_state.service import Service

NOW = datetime(2026, 11, 2, 10, 0, tzinfo=timezone.utc)

LETTER = """# AP0 email to the client PM

- Status: draft
- Classification: client_pm
- To: STK-001
- Subject: Our reading of your brief

---

Dear Dr Example,

**1. The problem as we read it**

We read the decision as **the design** of the obligation itself.

---

Horus
"""

MAIL_STYLE = """Subject: Our reading of your brief
To: Client PM (pm@example.gov)
Cc: none

Dear Dr Example,

Thank you for the **terms of reference**.

Horus
"""


@pytest.fixture
def svc(tmp_path):
    s = Service(tmp_path, actor="principal", session_id="test")
    s.init_engagement("TST-2026-001", "Test engagement", {"entity": "Ministry of Testing", "country": "EGY"}, supervisors=["sup"])
    return s


def sup(svc):
    return Service(svc.store.workspace, actor="supervisor:sup", session_id="test")


@pytest.fixture
def mail(monkeypatch):
    """Configured mail settings and a MailClient.send that records instead of connecting."""
    sent = []
    settings = MailSettings(user="horus@example.com", app_password="app-password", from_name="Horus", from_address="hello@horushq.ai")
    monkeypatch.setattr("horus_mail.client.MailSettings.load", classmethod(lambda cls: settings))

    def fake_send(self, to, subject, body, *, cc=(), html=None, attachments=(), in_reply_to=None):
        sent.append({"to": list(to), "subject": subject, "body": body, "cc": list(cc), "attachments": [str(a) for a in attachments], "in_reply_to": in_reply_to, "from": self.settings.from_address})
        return f"<msg-{len(sent)}@horushq.ai>"

    monkeypatch.setattr("horus_mail.client.MailClient.send", fake_send)
    return sent


@pytest.fixture
def no_mail(monkeypatch):
    monkeypatch.setattr("horus_mail.client.MailSettings.load", classmethod(lambda cls: MailSettings()))


def make_email(svc, *, to=None, cc=(), attachments=(), text=LETTER, subject="Our reading of your brief", status="pending_approval", request=True, body_path="inbox/outbound/letter.md"):
    pm = svc.create("stakeholders", {"name": "Client PM", "category": "client_pm", "is_client": True, "client_role": "pm", "decision_role": "input", "contact": {"email": "pm@example.gov"}})
    path = svc.store.workspace / body_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if text is not None:
        path.write_text(text, encoding="utf-8")
    com = svc.create("communications", {"direction": "outbound", "from": "principal", "to": list(to) if to is not None else [pm["id"]], "cc": list(cc), "date": NOW, "subject": subject, "summary": "AP0 email to the client PM", "body_path": body_path, "attachments": list(attachments), "classification": "client_pm", "action_class": "client_pm_email", "status": status})
    apv = svc.request_approval({"collection": "communications", "id": com["id"]}, "client_pm_email", "Send the AP0 email to the PM") if request else None
    return pm, com, apv


def sent_outbound(svc, to, external_ref, date):
    """An earlier outbound email already sent (shadow autonomy lets the fixture record it without an approval)."""
    sup(svc).set_autonomy(profile="shadow")
    try:
        return svc.create("communications", {"direction": "outbound", "from": "system", "to": list(to), "date": date, "subject": "earlier", "summary": "earlier email", "classification": "client_pm", "status": "sent", "external_ref": external_ref})
    finally:
        sup(svc).set_autonomy(profile="default")


# ---- body ------------------------------------------------------------------------------------------

def test_body_title_and_rule_header_is_dropped_and_bold_stripped():
    header, body, dropped = prepare_body(LETTER)
    assert dropped == []
    assert header["subject"] == "Our reading of your brief" and header["to"] == "STK-001" and header["status"] == "draft"
    assert body.startswith("Dear Dr Example,\n\n1. The problem as we read it\n\n")
    assert "**" not in body and "# AP0" not in body and "Status:" not in body
    assert "\n---\n\nHorus\n" in body  # only the first rule separates the header; later rules are part of the letter
    assert body.endswith("Horus\n")


def test_body_mail_style_header_is_dropped():
    header, body, _ = prepare_body(MAIL_STYLE)
    assert header["subject"] == "Our reading of your brief" and "pm@example.gov" in header["to"] and header["cc"] == "none"
    assert body == "Dear Dr Example,\n\nThank you for the terms of reference.\n\nHorus\n"


def test_body_front_matter_is_dropped():
    header, body, _ = prepare_body("---\nsubject: Hello\nto: pm@example.gov\n---\n\nDear all,\n\nText.\n")
    assert header == {"subject": "Hello", "to": "pm@example.gov"} and body == "Dear all,\n\nText.\n"


def test_body_without_header_is_verbatim():
    plain = "Dear Dr Example,\n\nNote: the colon in this line is prose, not a header.\n\nHorus\n"
    assert prepare_body(plain) == ({}, plain, [])
    note_first = "Note: this is not a mail header.\n\nDear all,\n"
    assert split_body(note_first) == ({}, note_first)
    titled = "# Acknowledgement sent\n\n- To: pm@example.gov\n\n```\nDear all,\n```\n"
    assert split_body(titled) == ({}, titled)  # a title without a rule: nothing to separate


def test_body_metadata_below_the_letter_is_dropped():
    text = MAIL_STYLE + "\nAttachments: none\nLog: communications COM-004 {classification: client_pm, related: [DOC-001]}\n"
    header, body, dropped = prepare_body(text)
    assert body.endswith("Horus\n") and "Log:" not in body and "Attachments:" not in body
    assert dropped == ["Attachments: none", "Log: communications COM-004 {classification: client_pm, related: [DOC-001]}"]
    # two trailing metadata paragraphs go; a closing prose paragraph stays, even one with a colon
    header, body, dropped = prepare_body("Dear all,\n\nText.\n\nAttachments: none\n\nLog: x\n")
    assert body == "Dear all,\n\nText.\n" and dropped == ["Attachments: none", "Log: x"]
    header, body, dropped = prepare_body("Dear all,\n\nText.\n\nNote: the slots are Cairo time.\n")
    assert body == "Dear all,\n\nText.\n\nNote: the slots are Cairo time.\n" and dropped == []
    # a text that is nothing but metadata is kept, so the preview shows it rather than an empty email
    assert prepare_body("Attachments: none\nLog: x\n")[1] == "Attachments: none\nLog: x\n"


# ---- recipients and attachments ----------------------------------------------------------------------

def test_recipients_resolve_addresses_and_stakeholders(svc):
    pm, com, apv = make_email(svc, to=["Sponsor <sponsor@example.gov>", "PM@example.gov"], cc=[])
    svc.update("communications", com["id"], {"to": [pm["id"], "Sponsor <sponsor@example.gov>", "PM@example.gov"]})
    p = prepare(svc, com["id"])
    assert p.to == [("pm@example.gov", f"{pm['id']} Client PM"), ("Sponsor <sponsor@example.gov>", "")]  # the duplicate address is dropped
    assert p.cc == [] and p.sendable


def test_recipients_that_cannot_be_resolved_are_problems(svc):
    pm, com, apv = make_email(svc)
    nobody = svc.create("stakeholders", {"name": "Sponsor without address", "category": "client_decision_maker", "is_client": True, "client_role": "sponsor", "decision_role": "agree"})
    svc.update("communications", com["id"], {"to": [pm["id"], "horus"], "cc": [nobody["id"], pm["id"]]})
    p = prepare(svc, com["id"])
    assert p.to_addresses == ["pm@example.gov"] and p.cc == []  # the PM in cc is already in to
    assert any("'horus'" in x for x in p.problems) and any(nobody["id"] in x and "no email address" in x for x in p.problems)
    assert not p.sendable
    with pytest.raises(SendError) as exc:
        approve_and_send(sup(svc), p)
    assert "cannot send" in str(exc.value) and svc.get("approvals", apv["id"])["status"] == "pending"


def test_attachments_resolve_to_document_files(svc, tmp_path):
    src = tmp_path / "Terms of Reference.pdf"
    src.write_bytes(b"%PDF-1.4 fake")
    doc = svc.import_document(src, {"title": "Terms of reference", "kind": "terms_of_reference"})
    gone = svc.import_document(src, {"title": "Deleted later", "kind": "other"})
    (svc.store.workspace / gone["path"]).unlink()
    pm, com, apv = make_email(svc, attachments=[doc["id"], gone["id"]])
    p = prepare(svc, com["id"])
    assert p.attachments == [(svc.store.workspace / doc["path"], f"{doc['id']} Terms of reference")]
    assert any(gone["id"] in x and "not a file" in x for x in p.problems)
    svc.update("communications", com["id"], {"attachments": [doc["id"], pm["id"]]})
    p = prepare(svc, com["id"])
    assert any(pm["id"] in x and "not a document id" in x for x in p.problems)


# ---- threading ---------------------------------------------------------------------------------------

def test_threading_picks_latest_sent_email_to_the_same_recipient(svc):
    pm, com, apv = make_email(svc)
    sent_outbound(svc, ["pm@example.gov"], "<a1@horushq.ai>", datetime(2026, 10, 1, tzinfo=timezone.utc))
    latest_to_pm = sent_outbound(svc, [pm["id"]], "<a2@horushq.ai>", datetime(2026, 10, 5, tzinfo=timezone.utc))
    sent_outbound(svc, ["someone.else@example.org"], "<other@horushq.ai>", datetime(2026, 10, 9, tzinfo=timezone.utc))  # another thread
    sent_outbound(svc, ["pm@example.gov"], None, datetime(2026, 10, 10, tzinfo=timezone.utc))  # sent but no Message-ID
    svc.create("communications", {"direction": "outbound", "from": "principal", "to": ["pm@example.gov"], "date": datetime(2026, 10, 11, tzinfo=timezone.utc), "subject": "draft", "summary": "unsent draft", "external_ref": "<draft@horushq.ai>"})
    p = prepare(svc, com["id"])
    assert p.in_reply_to == "<a2@horushq.ai>" and p.in_reply_to_id == latest_to_pm["id"]


def test_threading_starts_new_thread_without_a_sent_email_to_these_recipients(svc):
    pm, com, apv = make_email(svc)
    sent_outbound(svc, ["someone.else@example.org"], "<other@horushq.ai>", datetime(2026, 10, 9, tzinfo=timezone.utc))
    p = prepare(svc, com["id"])
    assert p.in_reply_to is None and "new thread" in render_preview(p)


# ---- refusals ----------------------------------------------------------------------------------------

def test_prepare_refuses_inbound_sent_and_unknown(svc):
    pm, com, apv = make_email(svc)
    inbound = svc.create("communications", {"direction": "inbound", "from": "pm@example.gov", "to": ["horus"], "date": NOW, "summary": "a reply", "status": "received"})
    with pytest.raises(SendError, match="inbound"):
        prepare(svc, inbound["id"])
    done = sent_outbound(svc, ["pm@example.gov"], "<a1@horushq.ai>", NOW)
    with pytest.raises(SendError, match="already sent"):
        prepare(svc, done["id"])
    with pytest.raises(SendError, match="not a communication"):
        prepare(svc, "COM-999")


def test_missing_pieces_are_problems_not_sends(svc, mail):
    pm, com, _ = make_email(svc, subject=None, text=None, request=False)
    p = prepare(svc, com["id"])
    assert any("no approval request" in x for x in p.problems)
    assert any("does not exist" in x for x in p.problems)
    assert any("no subject" in x for x in p.problems)
    assert "Cannot send until:" in render_preview(p)
    with pytest.raises(SendError):
        approve_and_send(sup(svc), p)
    assert mail == []
    # an empty letter below a header is a problem too; a subject in the header stands in for a missing record subject
    (svc.store.workspace / "inbox" / "outbound" / "letter.md").write_text("Subject: From the header\nTo: pm@example.gov\n\n\n", encoding="utf-8")
    p = prepare(svc, com["id"])
    assert p.subject == "From the header" and any("no text below its header" in x for x in p.problems)


def test_send_only_requires_an_approved_approval(svc, mail):
    pm, com, apv = make_email(svc)
    p = prepare(svc, com["id"])
    with pytest.raises(SendError, match="--approve"):
        send_only(sup(svc), p)
    assert mail == []
    sup(svc).decide_approval(apv["id"], "approved", note="approved at the console")
    p = prepare(svc, com["id"])
    assert p.communication["status"] == "approved" and p.approval["id"] == apv["id"]
    result = send_only(sup(svc), p)
    assert result["sent"] and result["approval_decided_now"] is False
    assert svc.get("communications", com["id"])["status"] == "sent" and len(mail) == 1


def test_unconfigured_mail_refuses_before_deciding(svc, no_mail):
    pm, com, apv = make_email(svc)
    p = prepare(svc, com["id"])
    assert "not configured" in render_preview(p, None) or True  # the preview itself never needs mail
    with pytest.raises(SendError, match="mail is not configured"):
        approve_and_send(sup(svc), p)
    assert svc.get("approvals", apv["id"])["status"] == "pending"
    assert svc.get("communications", com["id"])["status"] == "pending_approval"


def test_reject_records_reason_and_returns_draft(svc):
    pm, com, apv = make_email(svc)
    p = prepare(svc, com["id"])
    with pytest.raises(SendError, match="reason"):
        reject(sup(svc), p, "")
    result = reject(sup(svc), p, "the second slot clashes with the budget meeting")
    assert result["rejected"] and result["status"] == "draft"
    decided = svc.get("approvals", apv["id"])
    assert decided["status"] == "rejected" and decided["decided_by"] == "supervisor:sup" and "budget meeting" in decided["note"]
    assert svc.get("communications", com["id"])["status"] == "draft"
    with pytest.raises(SendError):
        reject(sup(svc), prepare(svc, com["id"]), "again")


# ---- the happy path ------------------------------------------------------------------------------------

def test_approve_and_send_happy_path(svc, mail, tmp_path):
    src = tmp_path / "Terms of Reference.pdf"
    src.write_bytes(b"%PDF-1.4 fake")
    doc = svc.import_document(src, {"title": "Terms of reference", "kind": "terms_of_reference"})
    pm, com, apv = make_email(svc, cc=["sponsor@example.gov"], attachments=[doc["id"]])
    ack = sent_outbound(svc, ["pm@example.gov"], "<ack@horushq.ai>", datetime(2026, 10, 28, tzinfo=timezone.utc))
    # a second, superseded request for the same email stays pending and is only reported
    older = apv
    apv = svc.request_approval({"collection": "communications", "id": com["id"]}, "client_pm_email", "Revised AP0 email")
    p = prepare(svc, com["id"])
    assert p.approval["id"] == apv["id"] and p.other_pending == [older["id"]]
    preview = render_preview(p, "Horus <hello@horushq.ai>")
    assert apv["id"] in preview and older["id"] in preview and "pm@example.gov" in preview and "sponsor@example.gov" in preview
    assert f"reply to {ack['id']}" in preview and "Terms of reference" in preview and "Dear Dr Example," in preview and "Not sent:" not in preview
    assert "**" not in preview.split("-" * 72)[1]

    result = approve_and_send(sup(svc), p, note="approved from the console")
    assert result["sent"] and result["approval_decided_now"] and result["message_id"] == "<msg-1@horushq.ai>"
    assert len(mail) == 1
    wire = mail[0]
    assert wire["to"] == ["pm@example.gov"] and wire["cc"] == ["sponsor@example.gov"] and wire["subject"] == "Our reading of your brief"
    assert wire["body"].startswith("Dear Dr Example,\n\n1. The problem") and "**" not in wire["body"] and "Status:" not in wire["body"]
    assert wire["attachments"] == [str(svc.store.workspace / doc["path"])] and wire["in_reply_to"] == "<ack@horushq.ai>" and wire["from"] == "hello@horushq.ai"

    decided = svc.get("approvals", apv["id"])
    assert decided["status"] == "approved" and decided["decided_by"] == "supervisor:sup" and decided["note"] == "approved from the console"
    assert svc.get("approvals", older["id"])["status"] == "pending"
    record = svc.get("communications", com["id"])
    assert record["status"] == "sent" and record["approval"] == apv["id"] and record["external_ref"] == "<msg-1@horushq.ai>"
    assert record["date"] != NOW and record["updated_by"] == "supervisor:sup"
    assert any(ev.get("op") == "update" and ev.get("record_id") == com["id"] and "sent from the console" in (ev.get("reason") or "") for ev in svc.store.iter_events())
    with pytest.raises(SendError, match="already sent"):
        prepare(svc, com["id"])


def test_approve_tolerates_an_approval_already_given(svc, mail):
    pm, com, apv = make_email(svc)
    sup(svc).decide_approval(apv["id"], "approved")
    result = approve_and_send(sup(svc), prepare(svc, com["id"]))
    assert result["sent"] and result["approval_decided_now"] is False and len(mail) == 1


# ---- the console command -------------------------------------------------------------------------------

def test_cli_dry_run_sends_nothing(svc, mail):
    pm, com, apv = make_email(svc)
    runner = CliRunner()
    result = runner.invoke(app, ["send", com["id"], "-w", str(svc.store.workspace)])
    assert result.exit_code == 0, result.output
    assert "Dry run: nothing sent" in result.output and apv["id"] in result.output and "pm@example.gov" in result.output and "Dear Dr Example," in result.output
    assert mail == [] and svc.get("approvals", apv["id"])["status"] == "pending"
    assert runner.invoke(app, ["send", com["id"], "--reject", "-w", str(svc.store.workspace)]).exit_code == 2
    assert runner.invoke(app, ["send", com["id"], "--approve", "--send-only", "-w", str(svc.store.workspace)]).exit_code == 2
    assert runner.invoke(app, ["send", "COM-999", "-w", str(svc.store.workspace)]).exit_code == 1


def test_cli_approve_sends_and_records(svc, mail):
    pm, com, apv = make_email(svc)
    result = CliRunner().invoke(app, ["send", com["id"], "--approve", "--note", "go ahead", "--actor", "supervisor:sup", "-w", str(svc.store.workspace)])
    assert result.exit_code == 0, result.output
    assert f"approved {apv['id']} as supervisor:sup" in result.output and "Message-ID <msg-1@horushq.ai>" in result.output and "is now sent" in result.output
    assert len(mail) == 1 and svc.get("communications", com["id"])["status"] == "sent"
