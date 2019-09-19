import json
from datetime import datetime


def format_datetime(value, format=None):
    if format == 'date':
        format = "%d.%m.%Y"
    elif format == 'time':
        format = "%H:%M"
    else:
        format = "%d.%m.%Y %H:%M"
    return value.strftime(format)


def to_json(inst, cls, extended):

    convert = {
        datetime: format_datetime
    }
    d = dict()
    for col in cls.__table__.columns:
        v = getattr(inst, col.name)
        if col.type.python_type in convert.keys() and v is not None:
            try:
                d[col.name] = convert[col.type.python_type](v)
            except:
                d[col.name] = "Error:  Failed to covert using", str(convert[col.type.python_type])
        elif v is None:
            d[col.name] = str()
        else:
            d[col.name] = v
    if extended:
        inst.jsonify(res=d)

    return d
