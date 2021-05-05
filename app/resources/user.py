from flask_restful import Resource, abort
from app.models.user import UserModel
from app.parsers.user import post_parser, put_parser


class UserRegister(Resource):
    """ /user/register - Register a new user."""
    @classmethod
    def post(cls):
        # Get the submitted data
        user_data = post_parser.parse_args(strict=True)
        # Check if this user already exists?
        if UserModel.find_by_email(user_data.email):
            abort(404, message=f"L'utilisateur avec l'email <{email}> existe déjà.")
        # Store user and generate access_token
        user = UserModel(*user_data)
        user.save()

        return {'user': user.json(), 'message': 'Votre compte a été créé avec succès.'}


class User(Resource):
    @classmethod
    def get(cls, _id: int):
        """ /user/<_id:int> - Get a user."""
        user = UserModel.find_by_id(_id)
        if not user:
            abort(404, message="Cet utilisateur n'existe pas.")
        return {'user': user.json()}

    @classmethod
    def put(cls, _id: int):
        """ /user/<_id:int> - Update a user."""
        user = UserModel.find_by_id(_id)
        if not user:
            abort(404, message="Cet utilisateur n'existe pas.")

        user_data = put_parser.parse_args(strict=True)
        user.firstname = user_data.firstname
        user.lastname = user_data.lastname
        user.address = user_data.address
        user.contacts = user_data.contacts
        user.photo = user_data.photo
        user.email = user_data.email

        user.save()

        return {'user': user.json(), 'messsage': 'Les infos ont été mises à jour avec succès.'}

    @classmethod
    def delete(cls, _id: int):
        """ /user/<_id:int> - Delete a user."""
        user = UserModel.find_by_id(_id)
        if not user:
            abort(404, message="Cet utilisateur n'existe pas.")

        user.delete()
        return {'message': 'Compte supprimé avec succès.'}


class UserList(Resource):
    """ /users - Get all users - (superuser)"""
    @classmethod
    def get(cls):
        return {'users': [user.json() for user in UserModel.find_all()]}
