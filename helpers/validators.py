import datetime

def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Date format should be YYYY-MM-DD")

def validate_recreation_link(link):
    if not link.startswith("https://www.recreation.gov/ticket/"):
        
        raise ValueError("Link should start with https://www.recreation.gov/ticket/")