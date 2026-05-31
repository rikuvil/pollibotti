import os

STATE_FILE = "state/last_run.txt"
STATE_DIR = os.path.dirname(STATE_FILE)

if STATE_DIR:
    os.makedirs(STATE_DIR, exist_ok=True)


def has_run_this_week(week_key: str) -> bool:
    try:
        if not os.path.exists(STATE_FILE):
            return False

        with open(STATE_FILE, "r") as f:
            return f.read().strip() == week_key
    except Exception as e:
        print("STATE READ ERROR:", e)
        return False


def mark_run(week_key: str):
    try:
        with open(STATE_FILE, "w") as f:
            f.write(week_key)
    except Exception as e:
        print("STATE WRITE ERROR:", e)