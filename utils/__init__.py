from uuid import uuid4
import json
from datetime import datetime
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = f"{os.getcwd()}/uploads"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def json_serializer(datetime_object):
    if isinstance(datetime_object, datetime):
        return datetime_object.__str__()


def json_dump_(datetime_object):
    return json.dumps(datetime_object, default=json_serializer).replace('"', '')


def generate_uuid() -> str:
    """Generates a unique identifier in string form. The length is 8."""
    return str(uuid4())[:8]


def saveFileUploaded(fileStorage, subFolder: str):
    """Persists an uploaded file in the uploads folder and generates a custom file name."""
    filename = f"{generate_uuid()}{os.path.splitext(fileStorage.filename)[1]}"
    if allowed_file(fileStorage.filename):
        fileStorage.save(os.path.join(f"{UPLOAD_FOLDER}/{subFolder}", filename))
        return filename


def remove_file_upload(file_path) -> None:
    """Delete the existing files in the uploads folder."""
    if os.path.exists(file_path):
        os.remove(file_path)
