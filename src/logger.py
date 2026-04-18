# src/logger.py
import json
import os

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs.json")

def log_event(event):

    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(event)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)