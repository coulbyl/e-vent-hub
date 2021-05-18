from flask_restful import Resource
from flask import send_from_directory
from utils import UPLOAD_FOLDER
from flask_jwt_extended import jwt_required


class Upload(Resource):
    @classmethod
    @jwt_required()
    def get(cls, filename: str, folder: str):  # client, event, organizer
        return send_from_directory(f"{UPLOAD_FOLDER}/{folder}", filename)
