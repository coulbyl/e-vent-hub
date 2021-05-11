from flask_restful import Resource, abort
from app.models.organizer import OrganizerModel
from app.parsers.organizer import post_parser, put_parser, reset_parser, login_parser
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token
from werkzeug.security import check_password_hash, generate_password_hash, safe_str_cmp
from datetime import datetime

# Error message
ACCOUNT_DOES_NOT_EXIST = "Désolé, le compte ({}) n'existe pas."
ACCOUNT_ALREADY_EXISTS = "Désolé, le compte ({}) existe déjà."
ACCOUNT_SUCCESSFULLY_CREATED = "Votre compte a été créé avec succès."
ACCOUNT_SUCCESSFULLY_UPDATED = "Informations mises à jour avec succès."
ACCOUNT_SUCCESSFULLY_DELETED = "Votre compte a été supprimé avec succès."


class OrganizerRegister(Resource):
    """ /organizer/register - Register a new organizer."""
    @classmethod
    def post(cls):
        # Get the submitted data
        data = post_parser.parse_args(strict=True)
        # Check if this organizer already exists?
        if OrganizerModel.find_by_email(email=data.email):
            abort(400, message=ACCOUNT_ALREADY_EXISTS.format(data.email))
        # Store organizer and generate access_token
        organizer = OrganizerModel(**data)
        organizer.save()
        access_token = create_access_token(identity=organizer._uuid, fresh=True)
        refresh_token = create_refresh_token(identity=organizer._uuid)

        return {
            'organizer': organizer.json(),
            'token': {'access_token': access_token, 'refresh_token': refresh_token},
            'message': ACCOUNT_SUCCESSFULLY_CREATED
        }, 201


class Organizer(Resource):
    @classmethod
    # @jwt_required()
    def get(cls, _id: int):
        """ /organizer/<_id:int> - Get a organizer."""
        organizer = OrganizerModel.find_by_id(_id=_id)

        if not organizer:
            abort(404, message=ACCOUNT_DOES_NOT_EXIST.format(_id))
        return organizer.json()

    @classmethod
    @jwt_required()
    def put(cls, _id: int):
        """ /organizer/<_id:int> - Update a organizer."""
        organizer_found = OrganizerModel.find_by_id(_id=_id)
        if organizer_found:
            data = put_parser.parse_args(strict=True)

            organizer_found.name = data.name
            organizer_found.email = data.email
            organizer_found.contacts = data.contacts
            organizer_found.photo = data.photo
            organizer_found.updated_at = datetime.utcnow()

            organizer_found.save()
            return {'messsage': ACCOUNT_SUCCESSFULLY_UPDATED}

        abort(400, message=ACCOUNT_DOES_NOT_EXIST.format(_id))

    @classmethod
    @jwt_required()
    def delete(cls, _id: int):
        """ /organizer/<_id:int> - Delete a organizer."""
        organizer_found = OrganizerModel.find_by_id(_id=_id)
        if organizer_found:
            organizer_found.delete()
            return {'message': ACCOUNT_SUCCESSFULLY_DELETED}

        abort(400, message=ACCOUNT_DOES_NOT_EXIST.format(_id))


class OrganizerList(Resource):
    """ /organizers - Get all organizers - (superorganizer)"""
    @classmethod
    @jwt_required()  # admin claims
    def get(cls):
        return {'organizers': [organizer.json() for organizer in OrganizerModel.find_all()]}


class OrganizerPasswordReset(Resource):
    """ /organizer/password-reset/<_id> - Reset organizer password"""
    @classmethod
    @jwt_required()
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
                return {'messsage': 'Mot de passe réinitialisé avec succès.'}
            abort(400, message="Un problème est survenu. Vérifiez votre mot de passe.")
        abort(400, message=ACCOUNT_DOES_NOT_EXIST.format(_id))


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
                "organizer": organizer.json(),
                "token": {"access_token": access_token, "refresh_token": refresh_token}
            }

        abort(401, message="Invalid credentials.")
