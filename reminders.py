import schedule
import time
import threading
import re
from datetime import datetime, timedelta

# We'll import speak here to avoid circular imports
_speak_fn = None

def set_speak(fn):
    global _speak_fn
    _speak_fn = fn

def _alert(message: str):
    if _speak_fn:
        _speak_fn(f"Reminder: {message}")
    else:
        print(f"🔔 REMINDER: {message}")

def parse_and_set_reminder(user_text: str) -> str:
    """
    Tries to detect reminder intent from the user's speech.
    Supports patterns like:
      - 'remind me in 5 minutes to drink water'
      - 'remind me at 6pm to call mom'
    Returns a confirmation string, or None if no reminder found.
    """
    user_text_lower = user_text.lower()

    # Pattern: "in X minutes"
    match = re.search(r"in (\d+) minute", user_text_lower)
    if match:
        minutes = int(match.group(1))
        task = _extract_task(user_text_lower)
        run_time = datetime.now() + timedelta(minutes=minutes)
        schedule.every(minutes).minutes.do(_one_time_alert, task).tag("reminder")
        return f"Got it! I'll remind you to {task} in {minutes} minutes."

    # Pattern: "in X hours"
    match = re.search(r"in (\d+) hour", user_text_lower)
    if match:
        hours = int(match.group(1))
        task = _extract_task(user_text_lower)
        schedule.every(hours).hours.do(_one_time_alert, task).tag("reminder")
        return f"Sure! Reminding you to {task} in {hours} hours."

    return None  # No reminder detected

def _extract_task(text: str) -> str:
    """Extracts the task from phrases like 'remind me to X' or 'remind me in N minutes to X'."""
    match = re.search(r"to (.+?)(?:\s+in\s+\d+|\s+at\s+\d+|$)", text)
    if match:
        return match.group(1).strip()
    return "do the task"

_triggered = set()

def _one_time_alert(task):
    """Fires the reminder once, then removes itself."""
    _alert(task)
    return schedule.CancelJob  # Remove this job after running

def run_scheduler():
    """Runs the scheduler in a background thread — won't block the main loop."""
    def _loop():
        while True:
            schedule.run_pending()
            time.sleep(5)

    thread = threading.Thread(target=_loop, daemon=True)
    thread.start()
