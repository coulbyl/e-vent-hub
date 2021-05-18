from flask_restful import Resource, abort
from models.event import EventModel
from models.user import UserModel
from parsers.event import post_parser, put_parser, active_parser, allow_parser
from datetime import datetime
from flask_jwt_extended import jwt_required
from resources.admin import admin_required
from resources.organizer import organizer_required
from resources.user import client_required

# Messages
from resources import ACCOUNT_DOES_NOT_EXIST, EVENT_DOES_NOT_EXIST, EVENT_SUCCESSFULLY_DELETED, EVENT_SUCCESSFULLY_UPDATED, SERVER_ERROR


class EventStore(Resource):
    """ /event/store - Store event"""
    @classmethod
    @jwt_required()
    @organizer_required
    def post(cls):
        data = post_parser.parse_args(strict=True)
        event = EventModel(**data)
        try:
            event.save()
            return event.json(), 201
        except Exception:
            abort(500, SERVER_ERROR)


class EventParticipant(Resource):
    """ /event/participant/<event_id>/<user_id>"""
    @classmethod
    @jwt_required()
    @client_required
    def post(cls, event_id: int, user_id: int):
        event = EventModel.find_by_id(_id=event_id)
        if event and event.remaining_places > 0:
            participant = UserModel.find_by_id(_id=user_id)
            if participant:
                event_data = event.json()
                participants = event_data['participants']
                participant_exists = [p for p in participants if p['_id'] == user_id]
                if len(participant_exists) == 0:
                    try:
                        event.add_participant(participant)
                        event.remaining_places -= 1
                        event.save()
                        return {"message": "Inscription terminée avec succès."}, 201
                    except Exception:
                        abort(500, SERVER_ERROR)
                abort(400, message='Vous êtes déjà inscrit à cet événement.')
            abort(404, message=ACCOUNT_DOES_NOT_EXIST)
        abort(401, message="Désolé, il n'y a plus de places disponibles pour cet événement.")

    @classmethod
    @jwt_required()
    @client_required
    def delete(cls, event_id: int, user_id: int):
        event = EventModel.find_by_id(_id=event_id)
        if event:
            participant = UserModel.find_by_id(_id=user_id)
            if participant:
                event_data = event.json()
                participants = event_data['participants']
                participant_exists = [p for p in participants if p['_id'] == user_id]
                if len(participant_exists) > 0:
                    try:
                        event.remove_participant(participant)
                        event.remaining_places += 1
                        event.save()
                        return {"message": "Inscription retirée avec succès."}, 201
                    except Exception:
                        abort(500, message=SERVER_ERROR)
                abort(400, message="Désolé, vous n'êtes pas inscrit à cet événement.")
            abort(404, message=ACCOUNT_DOES_NOT_EXIST)
        abort(404, message=EVENT_DOES_NOT_EXIST)


class Event(Resource):
    @classmethod
    @jwt_required()
    def get(cls, _id: int):
        """ /event/<id> - Get event."""
        event = EventModel.find_by_id(_id=_id)
        if not event:
            abort(404, message=EVENT_DOES_NOT_EXIST)
        return event.json()

    @classmethod
    @jwt_required()
    @organizer_required
    def put(cls, _id: int):
        """ /event/<id> - Update event."""
        event = EventModel.find_without_active(_id=_id)
        if event:
            data = put_parser.parse_args(strict=True)
            event.name = data.name
            event.location = data.location
            event.description = data.description
            event.price = data.price
            event.available_places = data.available_places
            event.start_at = data.start_at
            event.end_at = data.end_at
            event.image = data.image
            event.active = data.active
            event.updated_at = datetime.utcnow()
            try:
                event.save()
                return {'messsage': EVENT_SUCCESSFULLY_UPDATED}
            except Exception:
                abort(500, message=SERVER_ERROR)
        abort(400, message=EVENT_DOES_NOT_EXIST)

    @classmethod
    @jwt_required()
    @organizer_required
    def delete(cls, _id: int):
        """ /event/<id> - Delete event."""
        event = EventModel.find_without_active(_id=_id)
        if event:
            try:
                event.delete()
                return {'message': EVENT_SUCCESSFULLY_DELETED}
            except Exception:
                abort(500, message=SERVER_ERROR)
        abort(400, message=EVENT_DOES_NOT_EXIST)


class EventPublication(Resource):
    @classmethod
    @jwt_required()
    @organizer_required
    def put(cls, _id: int):
        """ /event/publication/<id> - published or unpublished event."""
        event = EventModel.find_without_active(_id=_id)
        if event:
            data = active_parser.parse_args(strict=True)
            event.active = data.active
            event.updated_at = datetime.utcnow()
            try:
                event.save()
                return {'messsage': EVENT_SUCCESSFULLY_UPDATED}
            except Exception:
                abort(500, message=SERVER_ERROR)
        abort(400, message=EVENT_DOES_NOT_EXIST)


class EventPublishedList(Resource):
    """ /events - Get published events"""
    @classmethod
    def get(cls):
        return {'events': [event.json() for event in EventModel.find_all()]}


class EventUnpublishedList(Resource):
    """ /events/unpublished - Get unpublished events """
    @classmethod
    def get(cls):
        return {'events': [event.json() for event in EventModel.find_all(active=False)]}


class EventAuthorization(Resource):
    @classmethod
    @jwt_required()
    @admin_required
    def put(cls, _id: int):
        """ /event/authorization/<id>"""
        event_found = EventModel.find_without_active(_id=_id)
        if event_found:
            data = allow_parser.parse_args(strict=True)
            event_found.allow = data.allow
            event_found.updated_at = datetime.utcnow()
            try:
                event_found.save()
                return {'messsage': EVENT_SUCCESSFULLY_UPDATED}
            except Exception:
                abort(500, message=SERVER_ERROR)
        abort(400, message=EVENT_DOES_NOT_EXIST)


class EventUnauthorizedList(Resource):
    """ /events/unauthorized - Get unauthorized events"""
    @classmethod
    def get(cls):
        return {'events': [event.json() for event in EventModel.find_allow(False)]}
