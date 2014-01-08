from datetime import datetime
import re

import json


class IOSFUEncoder(json.JSONEncoder):
    def default(self, obj):
        # DATETIME -> TIMESTAMP
        if isinstance(obj, datetime):
            return "timestamp:{}".format(to_timestamp(obj))

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def object_hook(s):
    for key in s:
        if isinstance(s[key], str):
            value = s[key]

            # TIMESTAMP -> DATETIME
            if value.startswith('timestamp:', 0, 10):
                timestamp = float(value[10:])
                s[key] = datetime.fromtimestamp(timestamp)

    return s


def slugify(string):
    """
    Slugify strings
    """
    string = string.lower()
    return re.sub(r'\W+', '-', string)


def serialize(dictionary):
    return json.dumps(dictionary, indent=4, cls=IOSFUEncoder)


def deserialize(string):
    return json.loads(string, object_hook=object_hook)


def to_timestamp(dt):
    epoch = datetime(1970, 1, 1)
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6
