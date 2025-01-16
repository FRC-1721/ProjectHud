from flask import Flask
from datetime import datetime


def time_ago(dt):
    if dt is None:
        return "Never updated"

    now = datetime.now()
    delta = now - dt
    seconds = delta.total_seconds()

    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif seconds < 3600:
        return f"{int(seconds // 60)} minute(s) ago"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hour(s) ago"
    else:
        return f"{int(seconds // 86400)} day ago"
