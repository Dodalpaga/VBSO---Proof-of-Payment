import phonenumbers
from phonenumbers import format_number, PhoneNumberFormat
import re
import pandas as pd

def pretty_format_phone(number, default_region="FR"):
    if pd.isna(number):
        return None
    num_str = str(number).replace(".0", "").strip()
    try:
        parsed = phonenumbers.parse(num_str, default_region)
    except phonenumbers.NumberParseException:
        return num_str
    intl = format_number(parsed, PhoneNumberFormat.INTERNATIONAL)
    intl = intl.replace("+", "(+")
    intl = intl.replace(" ", ") ", 1)
    intl = intl.replace(" ", ".")
    return intl

def clean_filename(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\d_-]", "_", s)
    return s