# Utility methods to use in another modules

from bson import json_util
import json

def parse_json(data):
    return json.loads(json_util.dumps(data))