#core/utils/helpers.py

from pathlib import Path
import uuid
from datetime import datetime

def format_number(num, decimals=2):
    return f"{num:.{decimals}f}"

def format_date(date, fmt="%Y-%m-%d"):
    return date.strftime(fmt)

def generate_id(prefix="id"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def safe_division(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 0

def normalize_string(text: str):
    return text.strip().lower().replace(" ", "_")
