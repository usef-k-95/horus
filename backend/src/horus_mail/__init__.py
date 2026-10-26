"""horus_mail — mail access the Gmail connector cannot provide: downloading attachments and calendar
invites by Gmail message id over IMAP, sending with attachments over SMTP, and parsing .ics invites."""

__all__ = ["MailClient", "MailSettings", "parse_ics", "save_attachments"]

from .client import MailClient, MailSettings, parse_ics, save_attachments  # noqa: E402
