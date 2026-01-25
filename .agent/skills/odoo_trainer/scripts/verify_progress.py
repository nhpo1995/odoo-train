#!/usr/bin/env python3
"""
verify_progress.py

Purpose:
    Checks the latest teaching log (e.g., teaching_logs/day_XX_session.md)
    to verify if the session is marked as "Completed".

Usage:
    python3 verify_progress.py [day_number]
    If day_number is not provided, it finds the latest log.
"""

import glob
import os
import re
import sys

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) # .agent/skills/odoo_trainer/scripts -> .agent
LOGS_DIR = os.path.join(BASE_DIR, 'learning', 'teaching_logs')

def get_latest_log_file():
    if not os.path.exists(LOGS_DIR):
        return None
    files = glob.glob(os.path.join(LOGS_DIR, 'day_*_session.md'))
    if not files:
        return None
    # Sort by modification time or name. Let's sort by day number in filename if possible, else modification time.
    # filename format: day_XX_session.md
    def extract_day(f):
        m = re.search(r'day_(\d+)_session.md', os.path.basename(f))
        return int(m.group(1)) if m else 0
    
    files.sort(key=extract_day, reverse=True)
    return files[0]

def check_completion(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check for "Status: ✅ Completed" or similar
    if "Status: ✅ Completed" in content or "Status: Completed" in content:
        return True
    return False

def main():
    target_day = None
    if len(sys.argv) > 1:
        target_day = sys.argv[1]

    log_file = None
    if target_day:
        possible_path = os.path.join(LOGS_DIR, f"day_{target_day}_session.md")
        # Handle day 05 vs 5
        if not os.path.exists(possible_path):
             possible_path = os.path.join(LOGS_DIR, f"day_{int(target_day):02d}_session.md")
        
        if os.path.exists(possible_path):
            log_file = possible_path
    else:
        log_file = get_latest_log_file()

    if not log_file:
        print("❌ No teaching log found.")
        sys.exit(1)

    print(f"Checking log: {log_file}")
    is_complete = check_completion(log_file)

    if is_complete:
        print("✅ Session Completed.")
        sys.exit(0)
    else:
        print("⚠️ Session In Progress (or not marked Completed).")
        sys.exit(1)

if __name__ == "__main__":
    main()
