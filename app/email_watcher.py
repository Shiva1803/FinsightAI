import time, email, imapclient, os
from . import ocr, extractor, db

def watch_mailbox(imap_host, imap_user, imap_pass, check_interval=60):
    # MVP: connect to IMAP, look for unseen messages with attachments, and process them
    try:
        client = imapclient.IMAPClient(imap_host, ssl=True, use_uid=True)
        client.login(imap_user, imap_pass)
        client.select_folder('INBOX')
        while True:
            messages = client.search(['UNSEEN'])
            for uid in messages:
                raw = client.fetch(uid, ['RFC822'])[uid][b'RFC822']
                msg = email.message_from_bytes(raw)
                for part in msg.walk():
                    if part.get_content_maintype()=='multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    filename = part.get_filename()
                    if not filename:
                        continue
                    content = part.get_payload(decode=True)
                    text = ocr.run_ocr_bytes(content, filename)
                    parsed = extractor.parse_document(text)
                    db.save_record(parsed, source_file=f"email:{filename}")
                client.add_flags(uid, ['\Seen'])
            time.sleep(check_interval)
    except Exception as e:
        print("Email watcher error (MVP):", e)
