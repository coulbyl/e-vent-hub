import functools
from flask_restful import Resource, abort
from flask_jwt_extended import (
    get_jwt, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity
)

from app.models.admin import AdminModel
from app.parsers.admin import post_parser, put_parser, reset_parser, login_parser, role_parser
from werkzeug.security import check_password_hash, safe_str_cmp, generate_password_hash
from datetime import datetime

# Error message
ADMIN_DOES_NOT_EXIST = "Désolé, l'utilisateur ({}) n'existe pas."
ADMIN_ALREADY_EXISTS = "Désolé, l'utilisateur ({}) existe déjà."
ADMIN_SUCCESSFULLY_CREATED = "Votre compte a été créé avec succès."
ADMIN_SUCCESSFULLY_UPDATED = "Informations mises à jour avec succès."
ADMIN_SUCCESSFULLY_DELETED = "Votre compte a été supprimé avec succès."


def admin_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        claims = get_jwt_identity()
        if claims['superuser'] == True and claims['admin'] == True:
            return func(*args, **kwargs)

        abort(401, message='Admin privilege required.')
    return wrapper


class AdminRegister(Resource):
    """ /admin/register - Register a new admin."""
    @classmethod
    @jwt_required()
    def post(cls):
        claims = get_jwt_identity()
        if claims['superuser'] == True and claims['admin'] == False:
            data = post_parser.parse_args(strict=True)

            if AdminModel.find_by_email(email=data.email):
                abort(400, message=ADMIN_ALREADY_EXISTS.format(data.email))

            admin = AdminModel(**data)
            admin.save()
            access_token = create_access_token(identity=admin._uuid, fresh=True)
            refresh_token = create_refresh_token(identity=admin._uuid)

            return {
                'admin': admin.json(),
                'token': {'access_token': access_token, 'refresh_token': refresh_token},
                'message': ADMIN_SUCCESSFULLY_CREATED
            }, 201
        abort(401, message='Superuser privilege rerquired.')


class Admin(Resource):
    @classmethod
    @jwt_required()
    @admin_required
    def get(cls, _id: int):
        """ /admin/<_id:int> - Get a admin."""
        #claims = get_jwt_identity()
        # if claims['superuser'] == True and claims['admin'] == True:
        admin = AdminModel.find_by_id(_id=_id)
        if not admin:
            abort(404, message=ADMIN_DOES_NOT_EXIST.format(_id))
        return admin.json()
        #abort(401, message='Admin privilege required.')

    @classmethod
    @jwt_required()
    def put(cls, _id: int):
        """ /admin/<_id:int> - Update a admin."""
        admin_found = AdminModel.find_by_id(_id=_id)
        if admin_found:
            data = put_parser.parse_args(strict=True)

            admin_found.username = data.username
            admin_found.email = data.email
            admin_found.contacts = data.contacts
            admin_found.updated_at = datetime.utcnow()
            admin_found.save()

            return {'messsage': ADMIN_SUCCESSFULLY_UPDATED}

        abort(400, message=ADMIN_DOES_NOT_EXIST.format(_id))

    @classmethod
    @jwt_required()
    def delete(cls, _id: int):
        """ /admin/<_id:int> - Delete a admin."""
        admin_found = AdminModel.find_by_id(_id=_id)
        if admin_found and admin_found.role == 'admin':
            admin_found.delete()
            return {'message': ADMIN_SUCCESSFULLY_DELETED}

        abort(400, message=ADMIN_DOES_NOT_EXIST.format(_id))


class AdminList(Resource):
    """ /admins - Get all admins - (superadmin)"""
    @classmethod
    @jwt_required()
    def get(cls):
        claims = get_jwt_identity()
        if not claims['is_superuser']:
            return {'message': 'Superuser privilege required.'}, 401

        return {'admins': [admin.json() for admin in AdminModel.find_all()]}


class AdminPasswordReset(Resource):
    """ /admin/reset-password/<_id> - Reset admin password"""
    @classmethod
    @jwt_required()
    def put(cls, _id: int):
        admin_found = AdminModel.find_by_id(_id=_id)
        if admin_found:
            data = reset_parser.parse_args(strict=True)
            is_same = check_password_hash(admin_found.password, data.old_password)
            if is_same and safe_str_cmp(data.new_password, data.confirm_password):
                admin_found.password = generate_password_hash(data.new_password)
                admin_found.updated_at = datetime.utcnow()
                admin_found.save()
                return {'messsage': 'Mot de passe réinitialisé avec succès.'}
            abort(400, message="Un problème est survenu. Vérifiez votre mot de passe.")
        abort(400, message=ADMIN_DOES_NOT_EXIST.format(_id))


class AdminLogin(Resource):
    """ /admin/login - Login a admin """
    @classmethod
    def post(cls):
        data: dict = login_parser.parse_args()
        admin = AdminModel.find_by_email(email=data.email)

        if admin and check_password_hash(admin.password, data.password):
            access_token = create_access_token(identity=admin._uuid, fresh=True)
            refresh_token = create_refresh_token(identity=admin._uuid)

            return {
                "admin": admin.json(),
                "token": {"access_token": access_token, "refresh_token": refresh_token}
            }

        abort(401, message="Invalid credentials.")


class AdminRole(Resource):
    @classmethod
    @jwt_required()
    def put(cls, _id: int):
        """ /admin/role/<_id:int> - Update a admin."""
        claims = get_jwt_identity()
        if not claims['is_superuser']:
            return {'message': 'Superuser privilege required.'}, 401

        admin_found = AdminModel.find_by_id(_id=_id)
        if admin_found and admin_found.role == 'admin':
            data = role_parser.parse_args(strict=True)
            admin_found.role = data.role
            admin_found.updated_at = datetime.utcnow()
            admin_found.save()
            return {'messsage': ADMIN_SUCCESSFULLY_UPDATED}
        abort(400, message=ADMIN_DOES_NOT_EXIST.format(_id))
