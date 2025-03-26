import datetime
import re

def parse_date(date_str):
    today = datetime.datetime.now()
    year = today.year

    if date_str == "내일":
        return today + datetime.timedelta(days=1)

    try:
        if re.match(r'^\d{1,2}[./]\d{1,2}$', date_str):
            parts = re.split(r'[./]', date_str)
            month, day = int(parts[0]), int(parts[1])
            return datetime.datetime(year, month, day)

        if re.match(r'^\d{1,2}월\s*\d{1,2}일$', date_str):
            date_str = date_str.replace('월', '.').replace('일', '')
            parts = date_str.split('.')
            month, day = int(parts[0]), int(parts[1])
            return datetime.datetime(year, month, day)

        if re.match(r'^\d{4}[./-]\d{1,2}[./-]\d{1,2}$', date_str):
            return datetime.datetime.strptime(date_str, "%Y.%m.%d")
    except:
        return None

    return None
