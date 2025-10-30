import time, email, imapclient, os, threading
from . import ocr, extractor, db

# Global state for email watcher
_watcher_thread = None
_watcher_running = False
_watcher_config = {}
_watcher_stats = {
    "status": "stopped",
    "emails_processed": 0,
    "last_check": None,
    "last_error": None
}

def watch_mailbox(imap_host, imap_user, imap_pass, check_interval=60):
    """Background task that monitors mailbox for new documents"""
    global _watcher_running, _watcher_stats
    
    _watcher_running = True
    _watcher_stats["status"] = "running"
    
    try:
        client = imapclient.IMAPClient(imap_host, ssl=True, use_uid=True)
        client.login(imap_user, imap_pass)
        client.select_folder('INBOX')
        
        while _watcher_running:
            try:
                messages = client.search(['UNSEEN'])
                _watcher_stats["last_check"] = time.strftime("%Y-%m-%d %H:%M:%S")
                
                for uid in messages:
                    raw = client.fetch(uid, ['RFC822'])[uid][b'RFC822']
                    msg = email.message_from_bytes(raw)
                    
                    for part in msg.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue
                        
                        filename = part.get_filename()
                        if not filename:
                            continue
                        
                        # Process attachment
                        content = part.get_payload(decode=True)
                        text = ocr.run_ocr_bytes(content, filename)
                        parsed = extractor.parse_document(text)
                        db.save_record(parsed, source_file=f"email:{filename}")
                        
                        _watcher_stats["emails_processed"] += 1
                    
                    client.add_flags(uid, [b'\\Seen'])
                
                time.sleep(check_interval)
                
            except Exception as e:
                _watcher_stats["last_error"] = str(e)
                print(f"Email check error: {e}")
                time.sleep(check_interval)
                
    except Exception as e:
        _watcher_stats["status"] = "error"
        _watcher_stats["last_error"] = str(e)
        print(f"Email watcher error: {e}")
    finally:
        _watcher_running = False
        if _watcher_stats["status"] != "error":
            _watcher_stats["status"] = "stopped"

def start_watcher(imap_host: str, imap_user: str, imap_pass: str, check_interval: int = 60):
    """Start the email watcher in a background thread"""
    global _watcher_thread, _watcher_config
    
    if _watcher_running:
        return {"error": "Watcher already running"}
    
    _watcher_config = {
        "imap_host": imap_host,
        "imap_user": imap_user,
        "check_interval": check_interval
    }
    
    _watcher_thread = threading.Thread(
        target=watch_mailbox,
        args=(imap_host, imap_user, imap_pass, check_interval),
        daemon=True
    )
    _watcher_thread.start()
    
    return {"status": "started"}

def stop_watcher():
    """Stop the email watcher"""
    global _watcher_running
    
    if not _watcher_running:
        return {"error": "Watcher not running"}
    
    _watcher_running = False
    return {"status": "stopped"}

def get_watcher_status():
    """Get current watcher status and stats"""
    return {
        "running": _watcher_running,
        "config": _watcher_config,
        "stats": _watcher_stats
    }
