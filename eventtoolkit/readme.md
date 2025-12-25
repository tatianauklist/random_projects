# Events Toolkit

A Python script that processes event submissions from Google Forms, tracks analytics, and identifies upcoming events with smart deduplication.

## What It Does

- 📝 Reads event submissions from a Google Form (via its response sheet)
- ✨ Filters out already-processed events (no duplicates!)
- 📊 Analyzes events by status and type
- 🔔 Identifies your next upcoming event
- 💾 Maintains state via JSON file (`processedEvents.json`)

## Current Status

**Phase:** Local Testing  
**Next Step:** Cloud Run deployment with service accounts

## Key Features

### 📊 Event Analytics
Automatically categorizes and counts events by:
- **Status** (Confirmed, Pending, Cancelled, etc.)
- **Type** (Conference, Workshop, etc.)

### 🔍 Smart Deduplication
Uses `processedEvents.json` to track which events have been analyzed. Only processes new events on subsequent runs.

### 📅 Next Event Detection
Automatically identifies the next upcoming event based on date, helping you stay on top of your schedule.

### 🪵 Detailed Logging
Comprehensive logging with timestamps for debugging and monitoring:
- Connection status
- Processing statistics
- Event counts (new vs skipped)
- Next upcoming event
- File operations

## Setup

### Prerequisites
- Python 3.8+
- Google Cloud Project
- Google Sheets API enabled
- A Google Form set up to collect event submissions
- Form responses linked to a Google Sheet

### Installation

```bash
# Clone the repo
git clone <repo-url>
cd events-toolkit

# Install dependencies
pip install -r requirements.txt

# Set up credentials
# Place your OAuth credentials.json in the project root
```

**requirements.txt:**
```
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
```

### Configuration

Update the script with your details:
```python
SHEETS_ID = 'your-spreadsheet-id'  # Form responses spreadsheet
RANGE = 'REF!A2:F'                 # Sheet name and data range
```

**Expected columns in your form responses:**
1. Event Date (MM-DD-YYYY format)
2. Event ID (unique identifier)
3. Event Size
4. Event Type
5. Event Status
6. Event Revenue

## Usage

```bash
python main.py
```

**Output:**
```
2024-12-20 14:30:01 - root - INFO - Connecting to Google Sheets API...
2024-12-20 14:30:03 - root - INFO - Done!, 15 events processed.
2024-12-20 14:30:03 - root - INFO - Status Counts: {'Confirmed': 8, 'Pending': 5, 'Cancelled': 2}
2024-12-20 14:30:03 - root - INFO - Type Counts: {'Conference': 6, 'Workshop': 9}
2024-12-20 14:30:03 - root - INFO - New Events: 3
2024-12-20 14:30:03 - root - INFO - Skipped Events: 12
2024-12-20 14:30:03 - root - INFO - Next Event: EVT_2024_123 on 12-25-2024
2024-12-20 14:30:03 - root - INFO - Writing results to file...
2024-12-20 14:30:03 - root - INFO - 3 events processed and added to processedEvents.json.
```

## How It Works

1. **Authenticate:** Sets up Google Sheets API credentials (uses `token.json` for subsequent runs)
2. **Fetch Form Submissions:** Reads event data from the specified sheet range
3. **Check State:** Reads `processedEvents.json` to see what's already been processed
4. **Filter New Events:** Only processes events not in the state file
5. **Analyze Events:** Counts events by status and type
6. **Find Next Event:** Identifies the closest upcoming event by date
7. **Update State:** Saves newly processed event IDs to JSON
8. **Log Results:** Outputs summary statistics and next upcoming event

## Workflow

```
User fills out form
        ↓
Form writes to "REF" sheet
        ↓
Script reads REF!A2:F range
        ↓
Script filters new events
        ↓
Script analyzes & counts
        ↓
Next event identified
        ↓
State saved to processedEvents.json
```

## File Structure

```
events-toolkit/
├── main.py                    # Main script
├── processedEvents.json       # State file (auto-generated)
├── credentials.json           # Google OAuth credentials
├── token.json                 # Auth token (auto-generated)
├── requirements.txt           # Dependencies
└── README.md                  # You are here
```

## State Persistence

The script maintains state in `processedEvents.json`:
```json
[
  "EVT_2024_001",
  "EVT_2024_002",
  "EVT_2024_003"
]
```

**Important:** This file must persist between runs to prevent duplicate processing and maintain accurate analytics.

## Roadmap

### Phase 1: Local Testing ✅
- [x] Read form responses from Sheets (REF sheet)
- [x] Event deduplication via state file
- [x] Status and type analytics
- [x] Upcoming event identification
- [x] Local state management (processedEvents.json)
- [x] Proper logging with timestamps

### Phase 2: Cloud Deployment 🚧
- [ ] Service account setup
- [ ] Migrate state to Cloud Storage/Firestore
- [ ] Deploy to Cloud Run
- [ ] Set up Cloud Scheduler for automation
- [ ] Implement Cloud Logging

### Phase 3: Enhancements 📋
- [ ] Email notifications for new high-priority events
- [ ] Revenue analytics and reporting
- [ ] Event filtering by status/type
- [ ] Dashboard visualization (web interface)
- [ ] Multiple sheets/forms support
- [ ] Export analytics to separate tracking sheet
- [ ] Backup/restore functionality

## Troubleshooting

**Events being reprocessed?**
- Check that `processedEvents.json` persists between runs
- Verify the event ID column contains unique identifiers
- Make sure the file isn't being deleted between script runs

**No data found warning?**
- Verify your `SHEETS_ID` is correct
- Check that form responses exist in the REF sheet
- Confirm the range `REF!A2:F` matches your sheet structure
- Make sure column headers are in row 1 (data starts at row 2)

**Next event not showing?**
- This is expected when there are no future events
- Verify event dates are in MM-DD-YYYY format
- Check that at least one event date is after today

**API authentication errors?**
- Delete `token.json` and re-authenticate
- Verify `credentials.json` is in the project root
- Ensure Google Sheets API is enabled in your GCP project

## Future: Cloud Run Deployment

When ready to deploy, the main changes will be:
1. Replace JSON file I/O with Cloud Storage or Firestore
2. Set up a service account with appropriate IAM permissions
3. Deploy container to Cloud Run
4. Schedule with Cloud Scheduler

## Contributing

This is a personal learning project as I work toward Google Cloud certification. Feedback and suggestions welcome!

## License

MIT

---

**Built with:** Python, Google Forms, Google Sheets API  
**Learning Focus:** Cloud automation, service accounts, stateful scripting