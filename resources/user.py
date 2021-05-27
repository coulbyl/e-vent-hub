import functools
from flask_restful import Resource, abort
from flask_jwt_extended import (
    get_jwt, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity
)

from models.user import UserModel
from models.event import EventModel
from models.token import TokenBlockList
from parsers.user import post_parser, put_parser, reset_parser, login_parser
from parsers.event import active_parser
from werkzeug.security import check_password_hash, safe_str_cmp, generate_password_hash
from datetime import datetime
from .admin import admin_required
from utils import remove_file_upload, saveFileUploaded, UPLOAD_FOLDER

# Message
from resources import (
    ACCOUNT_DOES_NOT_EXIST, ACCOUNT_ALREADY_EXISTS, ACCOUNT_SUCCESSFULLY_CREATED,
    ACCOUNT_SUCCESSFULLY_DELETED, ACCOUNT_SUCCESSFULLY_UPDATED, EVENT_DOES_NOT_EXIST,
    EXTENTION_ERROR, INVALIDCREDENTIALS, SERVER_ERROR)


def client_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        claims = get_jwt_identity()
        if not claims['client']:
            abort(401, message="Client privilege required.")

        return func(*args, **kwargs)
    return wrapper


class UserRegister(Resource):
    """ /user/register - Register a new user."""
    @classmethod
    def post(cls):
        data = post_parser.parse_args(strict=True)
        if UserModel.find_by_email(email=data.email):
            abort(400, message=ACCOUNT_ALREADY_EXISTS)
        user = UserModel(**data)
        if data['photo']:
            response = saveFileUploaded(data['photo'], 'client')
            print(response)
            if response is None:
                abort(400, message=EXTENTION_ERROR)
            user.photo = response

        try:
            user.save()
            access_token = create_access_token(identity=user._uuid, fresh=True)
            refresh_token = create_refresh_token(identity=user._uuid)

            return {
                'user': user.json(),
                'token': {'access_token': access_token, 'refresh_token': refresh_token},
                'message': ACCOUNT_SUCCESSFULLY_CREATED
            }, 201
        except Exception:
            abort(500, message=SERVER_ERROR)


class UserFavouriteEvent(Resource):
    """ /user/favourite-event/<int:user_id>/<int:event_id> - """
    @classmethod
    @jwt_required()
    @client_required
    def post(cls, user_id: int, event_id: int):
        user = UserModel.find_by_id(_id=user_id)
        if user:
            event = EventModel.find_by_id(_id=event_id)
            if event:
                try:
                    user.add_favourite(event)
                    return {"message": "Événement ajouté à votre liste de favoris."}, 201
                except Exception:
                    abort(500, message=SERVER_ERROR)
            abort(404, message=EVENT_DOES_NOT_EXIST)
        abort(404, message=ACCOUNT_DOES_NOT_EXIST)

    @classmethod
    @jwt_required()
    @client_required
    def delete(cls,  user_id: int, event_id: int):
        user = UserModel.find_by_id(_id=user_id)
        if user:
            event = EventModel.find_by_id(_id=event_id)
            if event:
                try:
                    user.remove_favourite(event)
                    return {"message": "Événement retiré à votre liste de favoris."}, 201
                except Exception:
                    abort(500, message=SERVER_ERROR)
            abort(404, message=EVENT_DOES_NOT_EXIST)
        abort(404, message=ACCOUNT_DOES_NOT_EXIST)


class User(Resource):
    @classmethod
    @jwt_required()
    def get(cls, _id: int):
        """ /user/<id> - Get a user."""
        user = UserModel.find_by_id(_id=_id)
        if not user:
            abort(404, message=ACCOUNT_DOES_NOT_EXIST)
        return user.json()

    @classmethod
    @jwt_required()
    @client_required
    def put(cls, _id: int):
        """ /user/<id> - Update a user."""
        user_found = UserModel.find_by_id(_id=_id)
        if user_found:
            existing_photo = user_found.photo
            data = put_parser.parse_args(strict=True)
            user_found.firstname = data.firstname
            user_found.lastname = data.lastname
            user_found.email = data.email
            user_found.contacts = data.contacts
            if data['photo']:
                response = saveFileUploaded(data['photo'], 'client')
                if response is None:
                    abort(400, message=EXTENTION_ERROR)
                user_found.photo = response
                remove_file_upload(f"{UPLOAD_FOLDER}/client/{existing_photo}")
            user_found.updated_at = datetime.utcnow()
            try:
                user_found.save()
                return {'message': ACCOUNT_SUCCESSFULLY_UPDATED}
            except Exception:
                abort(500, message=SERVER_ERROR)
        abort(400, message=ACCOUNT_DOES_NOT_EXIST)

    @classmethod
    @jwt_required()
    @client_required
    def delete(cls, _id: int):
        """ /user/<id> - Delete a user."""
        user = UserModel.find_by_id(_id=_id)
        if user:
            try:
                user.delete()
                return {'message': ACCOUNT_SUCCESSFULLY_DELETED}
            except Exception:
                abort(500, message=SERVER_ERROR)
        abort(400, message=ACCOUNT_DOES_NOT_EXIST)


class UserList(Resource):
    """ /users - Get all users - (superuser)"""
    @ classmethod
    # @jwt_required()  # admin claims
    def get(cls):
        return {'users': [user.json() for user in UserModel.find_all()]}


class UserPasswordReset(Resource):
    """ /user/reset-password/<_id> - Reset user password"""
    @classmethod
    @jwt_required()
    @client_required
    def put(cls, _id: int):
        user_found = UserModel.find_by_id(_id=_id)
        if user_found:
            data = reset_parser.parse_args(strict=True)
            is_same = check_password_hash(user_found.password, data.old_password)
            if is_same and safe_str_cmp(data.new_password, data.confirm_password):
                user_found.password = generate_password_hash(data.new_password)
                user_found.updated_at = datetime.utcnow()
                user_found.save()
                return {'message': 'Mot de passe réinitialisé avec succès.'}
            abort(400, message="Un problème est survenu. Vérifiez votre mot de passe.")
        abort(400, message=ACCOUNT_DOES_NOT_EXIST)


class UserLogin(Resource):
    """ /user/login - Login a user """
    @classmethod
    def post(cls):
        data: dict = login_parser.parse_args()
        user = UserModel.find_by_email(email=data.email)
        if user and check_password_hash(user.password, data.password):
            access_token = create_access_token(identity=user._uuid, fresh=True)
            refresh_token = create_refresh_token(identity=user._uuid)
            return {
                "user": user.json(),
                "token": {"access_token": access_token, "refresh_token": refresh_token}
            }
        abort(401, message=INVALIDCREDENTIALS)


class Logout(Resource):
    """ /logout - Logout a user """
    @classmethod
    @jwt_required()
    def delete(cls):
        jti = get_jwt()['jti']
        current_token = TokenBlockList(jti=jti)
        current_token.save()

        return {"message": "JWT révoqué et déconnexion de l'utilisateur réussie !"}


class TokenRefresh(Resource):
    """ /refresh - Refresh a token """
    @classmethod
    @jwt_required(refresh=True)
    def get(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}


class UserActivation(Resource):
    """ /user/activation/<id> - Activate or deactivate public user"""""
    @classmethod
    @jwt_required()
    @admin_required
    def put(cls, _id: int):
        args = active_parser.parse_args(strict=True)
        user = UserModel.find_without_active(_id)
        if user:
            user.active = args.active
            user.updated_at = datetime.utcnow()
            try:
                user.save()
                return {'message': ACCOUNT_SUCCESSFULLY_UPDATED}
            except Exception:
                abort(500, message=SERVER_ERROR)
        abort(400, message=ACCOUNT_DOES_NOT_EXIST)
