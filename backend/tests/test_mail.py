from email.message import EmailMessage

from horus_mail.client import find_meeting_link, parse_ics, safe_filename, save_attachments

ICS = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:abc123@google.com
DTSTART;TZID=Africa/Cairo:20261103T110000
DTEND;TZID=Africa/Cairo:20261103T114500
SUMMARY:Interview with the Deputy Minister
LOCATION:https://meet.google.com/abc-defg-hij
DESCRIPTION:Joining info\\nhttps://meet.google.com/abc-defg-hij\\n
 Second folded line
ORGANIZER;CN=PM:mailto:pm@example.gov
ATTENDEE;CN=Horus;PARTSTAT=NEEDS-ACTION:mailto:horus@example.com
END:VEVENT
END:VCALENDAR
"""


def test_parse_ics_extracts_meeting_link_and_times():
    ev = parse_ics(ICS)
    assert ev["dtstart"] == "20261103T110000" and ev["dtstart_tzid"] == "Africa/Cairo"
    assert ev["platform"] == "meet" and ev["meeting_link"] == "https://meet.google.com/abc-defg-hij"
    assert ev["summary"].startswith("Interview") and ev["attendees"][0]["email"] == "horus@example.com"
    assert "Second folded line" in ev["description"]


def test_find_links():
    assert find_meeting_link("join https://us02web.zoom.us/j/1234567890?pwd=abc now")[0] == "zoom"
    assert find_meeting_link("nothing here") == (None, None)


def test_save_attachments(tmp_path):
    msg = EmailMessage()
    msg["Subject"] = "docs"
    msg.set_content("see attached")
    msg.add_attachment(b"%PDF-1.4 fake", maintype="application", subtype="pdf", filename="Terms of Reference.pdf")
    msg.add_attachment(b"BEGIN:VCALENDAR", maintype="text", subtype="calendar", filename="invite.ics")
    saved = save_attachments(msg, tmp_path)
    names = sorted(p.name for p in saved)
    assert names == ["Terms of Reference.pdf", "invite.ics"]
    assert safe_filename("../../etc/passwd") == ".._.._etc_passwd"
