import os
import shutil
import zipfile
import datetime
import subprocess
import json
from pathlib import Path

# Load config.env values
config = {}
env_path = Path("config.env")
with open(env_path) as f:
    for line in f:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            config[key] = value

PROJECT_PATH = config["PROJECT_PATH"]
PROJECT_NAME = config["PROJECT_NAME"]
BACKUP_BASE = config["BACKUP_BASE"]
GDRIVE_REMOTE = config["GDRIVE_REMOTE"]
GDRIVE_FOLDER = config["GDRIVE_FOLDER"]

DAILY_RETENTION = int(config["DAILY_RETENTION"])
WEEKLY_RETENTION = int(config["WEEKLY_RETENTION"])
MONTHLY_RETENTION = int(config["MONTHLY_RETENTION"])

WEBHOOK_URL = config["WEBHOOK_URL"]
ENABLE_NOTIFY = config["ENABLE_NOTIFY"].lower() == "true"

# Create timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_filename = f"{PROJECT_NAME}_{timestamp}.zip"

# Create folder structure
today = datetime.datetime.now()
target_folder = Path(BACKUP_BASE) / str(today.year) / f"{today.month:02d}" / f"{today.day:02d}"
target_folder.mkdir(parents=True, exist_ok=True)

zip_path = target_folder / backup_filename

# Zip project directory
def zip_project(source, destination):
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, source)
                zipf.write(filepath, arcname)

zip_project(PROJECT_PATH, zip_path)

# Upload to Google Drive
subprocess.run([
    "rclone", "copy",
    str(zip_path),
    f"{GDRIVE_REMOTE}:{GDRIVE_FOLDER}"
], shell=True)

# Rotation cleanup function
def cleanup_rotation():
    base = Path(BACKUP_BASE)

    # Daily Retention
    all_daily = sorted(base.rglob("*.zip"), reverse=True)
    for old in all_daily[DAILY_RETENTION:]:
        old.unlink()

    # Weekly (Sunday)
    all_weeks = {}
    for file in sorted(base.rglob("*.zip")):
        date = datetime.datetime.strptime(file.stem.split("_")[-2], "%Y%m%d")
        if date.weekday() == 6:
            year_week = (date.year, date.isocalendar().week)
            all_weeks.setdefault(year_week, []).append(file)

    week_keys = sorted(all_weeks.keys(), reverse=True)
    for wk in week_keys[WEEKLY_RETENTION:]:
        for f in all_weeks[wk]:
            f.unlink()

    # Monthly
    all_months = {}
    for file in sorted(base.rglob("*.zip")):
        date = datetime.datetime.strptime(file.stem.split("_")[-2], "%Y%m%d")
        ym = (date.year, date.month)
        all_months.setdefault(ym, []).append(file)

    month_keys = sorted(all_months.keys(), reverse=True)
    for mk in month_keys[MONTHLY_RETENTION:]:
        for f in all_months[mk]:
            f.unlink()

cleanup_rotation()

# Logging
log_file = Path("logs/backup.log")
log_file.parent.mkdir(exist_ok=True)
with open(log_file, "a") as log:
    log.write(f"{timestamp} - Backup: {backup_filename} - Uploaded\n")

# Webhook notification
if ENABLE_NOTIFY:
    data = {
        "project": PROJECT_NAME,
        "date": timestamp,
        "status": "BackupSuccessful"
    }
    subprocess.run([
        "curl", "-X", "POST",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(data),
        WEBHOOK_URL
    ], shell=True)

import glob
from datetime import timedelta

def cleanup_old_backups():
    today = datetime.today().date()

    # Daily cleanup
    daily_files = sorted(glob.glob(f"{backup_base}\\*.zip"))
    if len(daily_files) > daily_retention:
        for file in daily_files[:-daily_retention]:
            os.remove(file)

# Run cleanup
cleanup_old_backups()

print("Backup completed successfully.")
