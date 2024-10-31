import imaplib
import email
from email.header import decode_header
import time
from dotenv import dotenv_values
from decorators import try_except

IMAP_SERVER = 'imap.gmail.com'

@try_except
def get_OTP():
    mails = get_unseen_emails()
    for mail in mails:
        if "OTP Code:" in mail:
            return mail.split("OTP Code:")[1]
    
    return None

@try_except
def get_unseen_emails():
    from datetime import datetime, timedelta
 
    config = dotenv_values(".env")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)

    mail.login(config.get("EMAIL"), config.get("EMAIL_PASSWORD"))

    mail.select("inbox")

    yesterday = (datetime.now() - timedelta(days=1)).strftime('%d-%b-%Y')  
    today = (datetime.now()).strftime('%d-%b-%Y')

    status, messages = mail.search(None, f'(FROM "noreply-prenotami@esteri.it" SINCE {today})')

    mails = []

    mail_ids = messages[0].split()

    if mail_ids:
        for mail_id in mail_ids[::-1]:
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
                                    mails.append(body)
                                except:
                                    pass
                    else:
                        body = msg.get_payload(decode=True).decode()
                        if body.startswith("OTP Code"):
                            mails.append(body)
    
    return mails