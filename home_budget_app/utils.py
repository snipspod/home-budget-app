# Utility methods to use in another modules

from bson import json_util
import json
from datetime import timedelta, datetime

def parse_json(data):
    return json.loads(json_util.dumps(data))

def last_day_of_month(date):
    next_month = date.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)