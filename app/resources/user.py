from flask_restful import Resource, abort
from flask_jwt_extended import (
    get_jwt, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity
)

from app.models.user import UserModel
from app.models.event import EventModel
from app.models.token import TokenBlockList
from app.parsers.user import post_parser, put_parser, reset_parser, login_parser
from werkzeug.security import check_password_hash, safe_str_cmp, generate_password_hash
from datetime import datetime

from flask import jsonify, make_response

# Error message
USER_DOES_NOT_EXIST = "Désolé, l'utilisateur ({}) n'existe pas."
EVENT_DOES_NOT_EXIST = "Désolé, l'évènement ({}) n'existe pas."
USER_ALREADY_EXISTS = "Désolé, l'utilisateur ({}) existe déjà."
ACCOUNT_SUCCESSFULLY_CREATED = "Votre compte a été créé avec succès."
ACCOUNT_SUCCESSFULLY_UPDATED = "Informations mises à jour avec succès."
ACCOUNT_SUCCESSFULLY_DELETED = "Votre compte a été supprimé avec succès."


class UserRegister(Resource):
    """ /register - Register a new user."""
    @classmethod
    def post(cls):
        # Get the submitted data
        data = post_parser.parse_args(strict=True)
        # Check if this user already exists?
        if UserModel.find_by_email(email=data.email):
            abort(400, message=USER_ALREADY_EXISTS.format(data.email))
        # Store user and generate access_token
        user = UserModel(**data)
        user.save()
        access_token = create_access_token(identity=user._id, fresh=True)
        refresh_token = create_refresh_token(identity=user._id)

        return {
            'user': user.json(),
            'token': {'access_token': access_token, 'refresh_token': refresh_token},
            'message': ACCOUNT_SUCCESSFULLY_CREATED
        }, 201


class UserFavouriteEvent(Resource):
    """ /user/favourite-event/<int:user_id>/<int:event_id> - """
    @classmethod
    @jwt_required()
    def post(cls, user_id: int, event_id: int):
        user_found = UserModel.find_by_id(_id=user_id)
        if user_found:
            event = EventModel.find_by_id(_id=event_id)
            if event:
                user_found.add_favourite(event)
                return {"message": "Événement ajouté à votre liste de favoris."}, 201
            abort(404, message=EVENT_DOES_NOT_EXIST.format(event_id))
        abort(404, message=USER_DOES_NOT_EXIST.format(user_id))

    @classmethod
    @jwt_required()
    def delete(cls,  user_id: int, event_id: int):
        user_found = UserModel.find_by_id(_id=user_id)
        if user_found:
            event = EventModel.find_by_id(_id=event_id)
            if event:
                user_found.remove_favourite(event)
                return {"message": "Événement retiré à votre liste de favoris."}, 201
            abort(404, message=EVENT_DOES_NOT_EXIST.format(event_id))
        abort(404, message=USER_DOES_NOT_EXIST.format(user_id))


class User(Resource):
    @classmethod
    @jwt_required()
    def get(cls, _id: int):
        """ /user/<_id:int> - Get a user."""
        user = UserModel.find_by_id(_id=_id)

        if not user:
            abort(404, message=USER_DOES_NOT_EXIST.format(_id))
        return user.json()

    @classmethod
    @jwt_required()
    def put(cls, _id: int):
        """ /user/<_id:int> - Update a user."""
        user_found = UserModel.find_by_id(_id=_id)
        if user_found:
            data = put_parser.parse_args(strict=True)

            user_found.firstname = data.firstname
            user_found.lastname = data.lastname
            user_found.email = data.email
            user_found.contacts = data.contacts
            user_found.photo = data.photo
            user_found.updated_at = datetime.utcnow()

            user_found.save()
            return {'messsage': ACCOUNT_SUCCESSFULLY_UPDATED}

        abort(400, message=USER_DOES_NOT_EXIST.format(_id))

    @classmethod
    @jwt_required()
    def delete(cls, _id: int):
        """ /user/<_id:int> - Delete a user."""
        user_found = UserModel.find_by_id(_id=_id)
        if user_found:
            user_found.delete()
            return {'message': ACCOUNT_SUCCESSFULLY_DELETED}

        abort(400, message=USER_DOES_NOT_EXIST.format(_id))


class UserList(Resource):
    """ /users - Get all users - (superuser)"""
    @classmethod
    @jwt_required()  # admin claims
    def get(cls):
        return {'users': [user.json() for user in UserModel.find_all()]}


class UserPasswordReset(Resource):
    """ /reset-password/<_id> - Reset user password"""
    @classmethod
    @jwt_required()
    def put(cls, _id: int):
        user_found = UserModel.find_by_id(_id=_id)
        if user_found:
            data = reset_parser.parse_args(strict=True)
            is_same = check_password_hash(user_found.password, data.old_password)
            if is_same and safe_str_cmp(data.new_password, data.confirm_password):
                user_found.password = generate_password_hash(data.new_password)
                user_found.updated_at = datetime.utcnow()
                user_found.save()
                return {'messsage': 'Mot de passe réinitialisé avec succès.'}
            abort(400, message="Un problème est survenu. Vérifiez votre mot de passe.")
        abort(400, message=USER_DOES_NOT_EXIST.format(_id))


class UserLogin(Resource):
    """ /login - Login a user """
    @classmethod
    def post(cls):
        data: dict = login_parser.parse_args()
        user = UserModel.find_by_email(email=data.email)

        if user and check_password_hash(user.password, data.password):
            access_token = create_access_token(identity=user._id, fresh=True)
            refresh_token = create_refresh_token(identity=user._id)

            return {
                "user": user.json(),
                "token": {"access_token": access_token, "refresh_token": refresh_token}
            }

        abort(401, message="Invalid credentials.")


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
