import functools
from flask_restful import Resource, abort
from flask_jwt_extended import (
    jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity
)

from models.admin import AdminModel
from parsers.admin import post_parser, put_parser, reset_parser, login_parser, role_parser
from werkzeug.security import check_password_hash, safe_str_cmp, generate_password_hash
from datetime import datetime

# Message
from resources import (
    ACCOUNT_DOES_NOT_EXIST, ACCOUNT_ALREADY_EXISTS, ACCOUNT_SUCCESSFULLY_CREATED,
    ACCOUNT_SUCCESSFULLY_DELETED, ACCOUNT_SUCCESSFULLY_UPDATED, INVALIDCREDENTIALS,
    SERVER_ERROR)


def superuser_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        claims = get_jwt_identity()
        if not claims['superuser']:
            abort(401, message="Superuser privilege required.")

        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        claims = get_jwt_identity()
        is_admin = claims['admin'] == True
        is_superuser = claims['superuser'] == True
        print(is_superuser, is_admin)
        if not is_superuser and not is_admin:
            abort(401, message="Admin privilege required.")

        return func(*args, **kwargs)
    return wrapper


class AdminRegister(Resource):
    """ /admin/register - Register a new admin."""
    @classmethod
    @jwt_required()
    @superuser_required
    def post(cls):
        data = post_parser.parse_args(strict=True)
        if AdminModel.find_by_email(email=data.email):
            abort(400, message=ACCOUNT_ALREADY_EXISTS.format(data.email))
        admin = AdminModel(**data)
        try:
            admin.save()
            return {
                'user': admin.json(),
                'message': ACCOUNT_SUCCESSFULLY_CREATED
            }, 201
        except Exception as e:
            abort(500, message=SERVER_ERROR.format(type(e).__name__))


class Admin(Resource):
    @classmethod
    @jwt_required()
    @admin_required
    def get(cls, _id: int):
        """ /admin/<_id:int> - Get a admin."""
        admin = AdminModel.find_by_id(_id=_id)
        if not admin:
            abort(404, message=ACCOUNT_DOES_NOT_EXIST)
        return admin.json()

    @classmethod
    @jwt_required()
    @admin_required
    def put(cls, _id: int):
        """ /admin/<id> - Update a admin."""
        admin_found = AdminModel.find_by_id(_id=_id)
        if admin_found:
            data = put_parser.parse_args(strict=True)
            admin_found.username = data.username
            admin_found.email = data.email
            admin_found.contacts = data.contacts
            admin_found.updated_at = datetime.utcnow()
            try:
                admin_found.save()
                return {'message': ACCOUNT_SUCCESSFULLY_UPDATED}
            except Exception as e:
                abort(500, message=SERVER_ERROR.format(type(e).__name__))
        abort(400, message=ACCOUNT_DOES_NOT_EXIST)

    @classmethod
    @jwt_required()
    @admin_required
    def delete(cls, _id: int):
        """ /admin/<id> - Delete a admin."""
        admin = AdminModel.find_by_id(_id=_id)
        if admin and admin.role == 'admin':
            try:
                admin.delete()
                return {'message': ACCOUNT_SUCCESSFULLY_DELETED}
            except Exception as e:
                abort(500, message=SERVER_ERROR.format(type(e).__name__))
        abort(400, message=ACCOUNT_DOES_NOT_EXIST)


class AdminList(Resource):
    """ /admins - Get all admins - (superadmin)"""
    @classmethod
    @jwt_required()
    @superuser_required
    def get(cls):
        return {'admins': [admin.json() for admin in AdminModel.find_all()]}


class AdminPasswordReset(Resource):
    """ /admin/password-reset/<_id> - Reset admin password"""
    @classmethod
    @jwt_required()
    @admin_required
    def put(cls, _id: int):
        admin_found = AdminModel.find_by_id(_id=_id)
        if admin_found:
            data = reset_parser.parse_args(strict=True)
            is_same = check_password_hash(admin_found.password, data.old_password)
            if is_same and safe_str_cmp(data.new_password, data.confirm_password):
                admin_found.password = generate_password_hash(data.new_password)
                admin_found.updated_at = datetime.utcnow()
                try:
                    admin_found.save()
                    return {'message': 'Mot de passe réinitialisé avec succès.'}
                except Exception as e:
                    abort(500, message=SERVER_ERROR.format(type(e).__name__))
            abort(400, message="Un problème est survenu. Vérifiez votre mot de passe.")
        abort(400, message=ACCOUNT_DOES_NOT_EXIST)


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
                "user": admin.json(),
                "token": {"access_token": access_token, "refresh_token": refresh_token}
            }

        abort(401, message=INVALIDCREDENTIALS)


class AdminRole(Resource):
    @classmethod
    @jwt_required()
    @superuser_required
    def put(cls, _id: int):
        """ /admin/role/<id> - Update a role of admin."""
        admin_found = AdminModel.find_by_id(_id=_id)
        if admin_found and admin_found.role == 'admin':
            data = role_parser.parse_args(strict=True)
            admin_found.role = data.role
            admin_found.updated_at = datetime.utcnow()
            try:
                admin_found.save()
                return {'message': ACCOUNT_SUCCESSFULLY_UPDATED}
            except Exception as e:
                abort(500, message=SERVER_ERROR.format(type(e).__name__))
        abort(400, message=ACCOUNT_DOES_NOT_EXIST)
