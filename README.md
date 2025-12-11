# Automated Backup and Google Drive Upload System

## Overview
This project provides a fully automated backup solution using Python and rclone.  
It creates timestamped ZIP backups of a local project folder, stores them in a structured directory, uploads them to Google Drive, sends a webhook notification, and runs daily through Windows Task Scheduler.

---

## Features
- Automatic ZIP backup creation  
- Timestamped backup naming  
- Organized local backup directory (Year/Month/Day)  
- Google Drive upload via rclone  
- Webhook notification after successful backup  
- Retention policy (daily/weekly/monthly cleanup)  
- Fully automated daily execution using Task Scheduler  

---

## Project Structure
BackupProject/
│
├── backup.py
├── config.env
├── logs/
└── local_backups/

---

## Local Backup Format
Backups are stored as:
local_backups/YYYY/MM/DD/MyProject_YYYYMMDD_HHMMSS.zip

---

## Configuration (config.env)
Example configuration:

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

## How It Works
1. Reads settings from **config.env**
2. Creates timestamped ZIP of the project folder
3. Saves the ZIP in the correct date folder
4. Uploads the ZIP to Google Drive using:
rclone copy ZIP_FILE gdrive:MyProjectBackups

5. Sends webhook notification (optional)
6. Applies retention cleanup for daily, weekly, monthly backups

---

## Running the Script Manually
Navigate to the project folder:
cd C:\Users\Siddesh\Desktop\BackupProject

makefile
Copy code

Run:
python backup.py

---

## Automating with Windows Task Scheduler
1. Open **Task Scheduler**
2. Create **New Basic Task**
3. Trigger: **Daily**
4. Action: **Start a Program**
5. Program/script:
C:\Users\Siddesh\AppData\Local\Programs\Python\Python312\python.exe

markdown
Copy code
6. Add arguments:
backup.py

markdown
Copy code
7. Start in:
C:\Users\Siddesh\Desktop\BackupProject

This ensures the backup runs every day automatically.

---

## Required Tools
- Python 3.12+
- rclone (configured with Google Drive)
- Webhook URL (optional)

---

## Screenshots (For Documentation)
Recommended screenshots:
- Local backup folder
- Google Drive folder showing uploaded ZIPs
- Task Scheduler configuration (General, Trigger, Action)
- Webhook request received
- Successful PowerShell execution of backup.py

---

## Output Example
Backup created: C:...\MyProject_20251211_162400.zip
Uploaded to Google Drive.
Notification sent.
Backup completed successfully.

---

## License
This project is for educational and demonstration purposes.
