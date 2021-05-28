from datetime import datetime
import functools
from utils import UPLOAD_FOLDER, remove_file_upload, saveFileUploaded
from flask_jwt_extended import (
    jwt_required, create_access_token,
    create_refresh_token, get_jwt_identity
)
from werkzeug.security import check_password_hash, generate_password_hash, safe_str_cmp
from flask_restful import Resource, abort

from models.organizer import OrganizerModel
from parsers.organizer import post_parser, put_parser, reset_parser, login_parser
from parsers.event import active_parser
from .admin import admin_required

# Message
from resources import (
    ACCOUNT_DOES_NOT_EXIST, ACCOUNT_ALREADY_EXISTS, ACCOUNT_SUCCESSFULLY_CREATED,
    ACCOUNT_SUCCESSFULLY_DELETED, ACCOUNT_SUCCESSFULLY_UPDATED, EXTENTION_ERROR,
    INVALIDCREDENTIALS, SERVER_ERROR)


def organizer_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        claims = get_jwt_identity()
        if not claims['organizer']:
            abort(401, message="Organizer privilege required.")

        return func(*args, **kwargs)
    return wrapper


class OrganizerRegister(Resource):
    """ /organizer/register - Register a new organizer."""
    @classmethod
    def post(cls):
        data = post_parser.parse_args(strict=True)
        if OrganizerModel.find_by_email(email=data.email):
            abort(400, message=ACCOUNT_ALREADY_EXISTS.format(data.email))
        organizer = OrganizerModel(**data)
        if data['photo']:
            response = saveFileUploaded(data['photo'], 'organizer')
            if response is None:
                abort(400, message=EXTENTION_ERROR)
            organizer.photo = response
        try:
            organizer.save()
            access_token = create_access_token(identity=organizer._uuid, fresh=True)
            refresh_token = create_refresh_token(identity=organizer._uuid)

            return {
                'user': organizer.json(),
                'token': {'access_token': access_token, 'refresh_token': refresh_token},
                'message': ACCOUNT_SUCCESSFULLY_CREATED
            }, 201
        except Exception as e:
            abort(500, message=SERVER_ERROR.format(type(e).__name__))


class Organizer(Resource):
    @classmethod
    @jwt_required()
    def get(cls, _id: int):
        """ /organizer/<id> - Get a organizer."""
        organizer = OrganizerModel.find_by_id(_id=_id)
        if not organizer:
            abort(404, message=ACCOUNT_DOES_NOT_EXIST)
        return organizer.json()

    @classmethod
    @jwt_required()
    @organizer_required
    def put(cls, _id: int):
        """ /organizer/<id> - Update a organizer."""
        organizer_found = OrganizerModel.find_by_id(_id=_id)
        if organizer_found:
            existing_photo = organizer_found.photo
            data = put_parser.parse_args(strict=True)
            organizer_found.name = data.name
            organizer_found.email = data.email
            organizer_found.contacts = data.contacts
            if data['photo']:
                response = saveFileUploaded(data['photo'], 'organizer')
                if response is None:
                    abort(400, message=EXTENTION_ERROR)
                organizer_found.photo = response
                remove_file_upload(f"{UPLOAD_FOLDER}/organizer/{existing_photo}")
            organizer_found.updated_at = datetime.utcnow()

            try:
                organizer_found.save()
                return {'message': ACCOUNT_SUCCESSFULLY_UPDATED}
            except Exception as e:
                abort(500, message=SERVER_ERROR.format(type(e).__name__))
        abort(400, message=ACCOUNT_DOES_NOT_EXIST)

    @classmethod
    @jwt_required()
    @organizer_required
    def delete(cls, _id: int):
        """ /organizer/<id> - Delete a organizer."""
        organizer = OrganizerModel.find_by_id(_id=_id)
        if organizer:
            try:
                organizer.delete()
                return {'message': ACCOUNT_SUCCESSFULLY_DELETED}
            except Exception as e:
                abort(500, message=SERVER_ERROR.format(type(e).__name__))
        abort(400, message=ACCOUNT_DOES_NOT_EXIST)


class OrganizerList(Resource):
    """ /organizers - Get all organizers - (superorganizer)"""
    @classmethod
    @jwt_required()
    @admin_required
    def get(cls):
        return {'organizers': [organizer.json() for organizer in OrganizerModel.find_all()]}


class OrganizerPasswordReset(Resource):
    """ /organizer/password-reset/<_id> - Reset organizer password"""
    @classmethod
    @jwt_required()
    @organizer_required
    def put(cls, _id: int):
        organizer_found = OrganizerModel.find_by_id(_id=_id)
        if organizer_found:
            data = reset_parser.parse_args(strict=True)
            is_same = check_password_hash(
                organizer_found.password, data.old_password)
            if is_same and safe_str_cmp(data.new_password, data.confirm_password):
                organizer_found.password = generate_password_hash(data.new_password)
                organizer_found.updated_at = datetime.utcnow()
                organizer_found.save()
                return {'message': 'Mot de passe réinitialisé avec succès.'}
            abort(400, message="Un problème est survenu. Vérifiez votre mot de passe.")
        abort(400, message=ACCOUNT_DOES_NOT_EXIST)


class OrganizerLogin(Resource):
    """ /organizer/login - Login a organizer """
    @classmethod
    def post(cls):
        data: dict = login_parser.parse_args()
        organizer = OrganizerModel.find_by_email(email=data.email)
        if organizer and check_password_hash(organizer.password, data.password):
            access_token = create_access_token(identity=organizer._uuid, fresh=True)
            refresh_token = create_refresh_token(identity=organizer._uuid)
            return {
                "user": organizer.json(),
                "token": {"access_token": access_token, "refresh_token": refresh_token}
            }
        abort(401, message=INVALIDCREDENTIALS)


class OrganizerActivation(Resource):
    """ /organizer/activation/<id> - Activate or deactivate organizer"""""
    @classmethod
    @jwt_required()
    @admin_required
    def put(cls, _id: int):
        args = active_parser.parse_args(strict=True)
        organizer = OrganizerModel.find_without_active(_id)
        if organizer:
            organizer.active = args.active
            organizer.updated_at = datetime.utcnow()
            try:
                organizer.save()
                return {'message': ACCOUNT_SUCCESSFULLY_UPDATED}
            except Exception as e:
                abort(500, message=SERVER_ERROR.format(type(e).__name__))
        abort(400, message=ACCOUNT_DOES_NOT_EXIST)
