import json

def log_event(event):
    with open("logs.json", "a") as f:
        f.write(json.dumps(event) + "\n")