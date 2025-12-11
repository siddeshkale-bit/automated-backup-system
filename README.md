# Automated Backup Script with Google Drive Integration

## Overview
This project automates the process of backing up a local project directory, storing backups in a structured timestamped format, uploading them to Google Drive using rclone, sending webhook notifications, and applying a retention policy to clean old backups.  
The backup runs manually or automatically using Windows Task Scheduler.

---

## How to Run the Script
Navigate to your project folder:

cd C:\Users\Siddesh\Desktop\BackupProject

Run the script:

python backup.py


---

## Arguments (Optional)
You can disable webhook notification using:

python backup.py --no-notify


(If implemented; else script uses config.env settings.)

---

## Installation and Configuration of rclone
### 1. Install rclone
Download the Windows installer from:
https://rclone.org/downloads/

Extract the folder and place `rclone.exe` inside:
C:\Windows\


Verify installation:

rclone version

makefile
Copy code

### 2. Configure Google Drive Remote
Run:

rclone config

markdown
Copy code

Then:
- Select **n** (new remote)
- Name it: `gdrive`
- Choose storage type: **Google Drive**
- Choose **auto config**
- Login to Google account
- Save configuration

Your remote will appear as:
[gdrive]
type = drive
scope = drive
token = {...}


---

## Configuration File (config.env)
Create a file named `config.env`:

PROJECT_PATH=C:\Users\Siddesh\Desktop\MyProject
PROJECT_NAME=Myproject
BACKUP_BASE=C:\Users\Siddesh\Desktop\BackupProject\local_backups
GDRIVE_REMOTE=gdrive
GDRIVE_FOLDER=MyProjectBackups
DAILY_RETENTION=7
WEEKLY_RETENTION=4
MONTHLY_RETENTION=3
WEBHOOK_URL=https://webhook.site/YOUR-UNIQUE-URL
ENABLE_NOTIFY=true


---

## Retention Settings
Retention values in `config.env` define how many backups are kept:

DAILY_RETENTION=7
WEEKLY_RETENTION=4
MONTHLY_RETENTION=3


Older backups beyond these limits are automatically deleted during script execution.

---

## Example Output
When the script completes successfully, example output:

Backup created: C:...\MyProject_20251211_100025.zip
Uploaded to Google Drive.
Webhook notification sent.
Backup completed successfully.

bash
Copy code

Google Drive will contain uploaded ZIP files, and the webhook will log:

{"project": "Myproject", "status": "BackupSuccessful"}

---

## Sample cURL Webhook Payload
This is sent when backup is successful:

curl -X POST -H "Content-Type: application/json"
-d '{"project":"Myproject","date":"20251211_100025","status":"BackupSuccessful"}'
https://webhook.site/YOUR-UNIQUE-URL


---

## Windows Task Scheduler (Automation)
To automate the script daily:

Program/script:
C:\Users\Siddesh\AppData\Local\Programs\Python\Python312\python.exe

sql
Copy code

Add arguments:
backup.py

powershell
Copy code

Start in:
C:\Users\Siddesh\Desktop\BackupProject

This runs the backup every day at the scheduled time.
---
## Security Considerations
- Keep `config.env` private — it contains sensitive paths and webhook URL.  
- Do **not** commit your webhook URL publicly.  
- Avoid giving write access to entire Google Drive; use a dedicated backup folder.  
- Ensure deletion permissions in rclone remote are properly restricted.  
