# utils/
# date_ranges

from django.utils.timezone import localdate
from datetime import timedelta

def get_today():
    return localdate()

def get_yesterday():
    return localdate() - timedelta(days=1)

def get_last_week_range():
    hoy = localdate()
    start = (hoy - timedelta(hoy.weekday())) - timedelta(weeks=1)
    end = start + timedelta(days=6)
    return start, end
