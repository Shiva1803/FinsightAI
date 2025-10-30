# Email Watcher Feature

## Overview
The Email Watcher automatically monitors your email inbox for new invoices and purchase orders, extracts data using OCR and AI, and saves them to your database.

## Features
- ✅ Real-time email monitoring via IMAP
- ✅ Automatic document processing
- ✅ OCR text extraction
- ✅ AI-powered data extraction
- ✅ Live status dashboard
- ✅ Statistics tracking

## Setup

### 1. Backend API Endpoints
The following endpoints are available:

- `POST /email/watch/start/` - Start the email watcher
- `POST /email/watch/stop/` - Stop the email watcher
- `GET /email/watch/status/` - Get current status and statistics

### 2. Frontend Page
Access the Email Watcher at: `http://localhost:5173/email-watcher`

### 3. Gmail Setup (Recommended)
1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Generate a new app password
3. Use this password in the Email Watcher configuration

### 4. Configuration
Fill in the form with:
- **IMAP Host**: `imap.gmail.com` (for Gmail)
- **Email Address**: Your email address
- **Password**: Your app password (not regular password)
- **Check Interval**: How often to check for new emails (in seconds)

## Usage

### Start Watching
1. Navigate to `/email-watcher` in the web interface
2. Fill in your email credentials
3. Click "Start Watching"
4. The system will check for new emails every 60 seconds (or your configured interval)

### Monitor Status
The status card shows:
- Running/Stopped status
- Number of emails processed
- Last check time
- Any errors encountered

### Stop Watching
Click the "Stop Watcher" button to stop monitoring

## How It Works

1. **Email Detection**: Connects to your IMAP mailbox and searches for unseen messages
2. **Attachment Processing**: Extracts PDF/image attachments from emails
3. **OCR Extraction**: Runs OCR on the attachments to extract text
4. **Data Parsing**: Uses AI to extract structured data (vendor, amounts, dates, etc.)
5. **Database Storage**: Saves the extracted data to your database
6. **Mark as Read**: Marks processed emails as read

## Security Notes

⚠️ **Important**: This is an MVP implementation. For production use:
- Store credentials securely (encrypted database or secrets manager)
- Use OAuth2 instead of passwords
- Implement proper authentication and authorization
- Add rate limiting
- Use HTTPS for all connections

## Troubleshooting

### "Authentication failed"
- Make sure you're using an App Password, not your regular password
- Check that IMAP is enabled in your email settings

### "Connection timeout"
- Verify the IMAP host is correct
- Check your firewall settings
- Ensure port 993 (IMAP SSL) is not blocked

### "No emails processed"
- Make sure emails have attachments (PDF or images)
- Check that emails are marked as unread
- Verify the email contains invoice/PO documents

## API Examples

### Start Watcher
```bash
curl -X POST http://localhost:8000/email/watch/start/ \
  -F "imap_host=imap.gmail.com" \
  -F "imap_user=your-email@gmail.com" \
  -F "imap_pass=your-app-password" \
  -F "check_interval=60"
```

### Get Status
```bash
curl http://localhost:8000/email/watch/status/
```

### Stop Watcher
```bash
curl -X POST http://localhost:8000/email/watch/stop/
```

## Response Format

### Status Response
```json
{
  "running": true,
  "config": {
    "imap_host": "imap.gmail.com",
    "imap_user": "your-email@gmail.com",
    "check_interval": 60
  },
  "stats": {
    "status": "running",
    "emails_processed": 5,
    "last_check": "2025-10-31 14:30:00",
    "last_error": null
  }
}
```
