from flask_restful import Resource, abort
from app.models.event import EventModel
from app.parsers.event import post_parser, put_parser, active_parser

# Error message
EVENT_DOES_NOT_EXIST = "Désolé, l'évènement ({}) n'existe pas."
EVENT_ALREADY_EXISTS = "Désolé, l'évènement ({}) existe déjà."
EVENT_SUCCESSFULLY_CREATED = "Votre évènement a été créé avec succès."
EVENT_SUCCESSFULLY_UPDATED = "Informations mises à jour avec succès."
EVENT_SUCCESSFULLY_DELETED = "Votre évènement a été supprimé avec succès."


class EventStore(Resource):
    """ /event/store - Store event"""
    @classmethod
    def post(cls):
        data = post_parser.parse_args(strict=True)
        event = EventModel(**data)
        event.save()

        return event.json(), 201


class Event(Resource):
    @classmethod
    def get(cls, _id: int):
        """ /event/<_id:int> - Get event."""
        event = EventModel.find_by_id(_id=_id)

        if not event:
            abort(404, message=EVENT_DOES_NOT_EXIST.format(_id))
        return event.json()

    @classmethod
    def put(cls, _id: int):
        """ /event/<_id:int> - Update event."""
        event_found = EventModel.find_by_id(_id=_id)
        if event_found:
            data = put_parser.parse_args(strict=True)

            event_found.name = data.name
            event_found.location = data.location
            event_found.description = data.description
            event_found.price = data.price
            event_found.available_places = data.available_places
            event_found.start_at = data.start_at
            event_found.end_at = data.end_at
            event_found.image = data.image
            event_found.active = data.active
            event_found.save()

            return {'messsage': EVENT_SUCCESSFULLY_UPDATED}

        abort(400, message=EVENT_DOES_NOT_EXIST.format(_id))

    @classmethod
    def delete(cls, _id: int):
        """ /event/<_id:int> - Delete event."""
        event_found = EventModel.find_by_id(_id=_id)
        if event_found:
            event_found.delete()
            return {'message': EVENT_SUCCESSFULLY_DELETED}

        abort(400, message=EVENT_DOES_NOT_EXIST.format(_id))


class EventPublication(Resource):
    @classmethod
    def put(cls, _id: int):
        """ /event/publication/<int:_id> - published or unpublished event."""
        event_found = EventModel.find_for_published(_id=_id)
        if event_found:
            data = active_parser.parse_args(strict=True)
            event_found.active = data.active
            event_found.save()
            return {'messsage': EVENT_SUCCESSFULLY_UPDATED}
        abort(400, message=EVENT_DOES_NOT_EXIST.format(_id))


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
