import imaplib
import email
from email.header import decode_header
import time
from dotenv import dotenv_values
from decorators import try_except

IMAP_SERVER = 'imap.gmail.com'

@try_except
def get_OTP():
    for mail in get_unseen_emails:
        if "OTP Code:" in mail:
            return int(mail.split("OTP Code:")[1])

@try_except
def get_unseen_emails():
    config = dotenv_values(".env")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)

    mail.login(config.get("EMAIL"), config.get("EMAIL_PASSWORD"))

    mail.select("inbox")

    status, messages = mail.search(None, '(UNSEEN)')

    mails = []

    mail_ids = messages[0].split()

    if mail_ids:
        for mail_id in mail_ids:
            status, msg_data = mail.fetch(mail_id, '(RFC822)')

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]

                    if isinstance(subject, bytes):
                        subject = subject.decode(
                            encoding if encoding else 'utf-8')

                    from_ = msg.get("From")

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            if "attachment" not in content_disposition:
                                try:
                                    body = part.get_payload(
                                    decode=True).decode()
                                    print("Contenido del correo:")
                                    mails.append(body)
                                except:
                                    pass
                    else:
                        content_type = msg.get_content_type()
                        body = msg.get_payload(decode=True).decode()
                        mails.append(body)
    
    return mails




