from uuid import uuid4
import json
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def json_serializer(datetime_object):
    if isinstance(datetime_object, datetime):
        return datetime_object.__str__()


def json_dump_(datetime_object):
    return json.dumps(datetime_object, default=json_serializer).replace('"', '')


def generate_uuid():
    return str(uuid4())[:8]
