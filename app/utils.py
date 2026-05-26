import re
import uuid
from datetime import datetime


def new_id(prefix: str) -> str:
    return f"{prefix}{uuid.uuid4().hex[:12]}"


def iso_to_dot(date_str: str) -> str:
    if not date_str:
        return date_str
    if "." in date_str and "-" not in date_str[:4]:
        return date_str
    return date_str.replace("-", ".")


def normalize_dot_date(date_str: str) -> str:
    """表单 ISO 或点分 → 存储用 YYYY.MM.DD（体重记录保持 YYYY-MM）。"""
    if not date_str:
        return date_str
    if re.fullmatch(r"\d{4}-\d{2}", date_str):
        return date_str
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
        return iso_to_dot(date_str)
    if "." in date_str:
        return date_str
    return date_str


def year_from_date(date_str: str) -> int:
    normalized = date_str.replace(".", "-")
    try:
        return int(normalized[:4])
    except ValueError:
        return datetime.utcnow().year
