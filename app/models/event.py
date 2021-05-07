from db import db
from datetime import datetime
from werkzeug.security import generate_password_hash
from utils import json_dump_


class EventModel(db.Model):
    __tablename__ = 'events'

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(250))
    price = db.Column(db.Float)
    available_places = db.Column(db.Integer, nullable=False)
    remaining_places = db.Column(db.Integer, nullable=False)
    start_at = db.Column(db.String(80), nullable=False)
    end_at = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(120))
    active = db.Column(db.Boolean, default=False, nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey(
        'organizers._id'), nullable=False)
    organizer = db.relationship('OrganizerModel', back_populates="events")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime)

    def __init__(
        self, name, location, description, price,
        available_places, start_at, end_at, image, organizer_id
    ):
        self.name = name
        self.location = location
        self.description = description
        self.price = price
        self.available_places = available_places
        self.remaining_places = available_places
        self.start_at = start_at
        self.end_at = end_at
        self.image = image
        self.organizer_id = organizer_id

    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'location': self.location,
            'description': self.description,
            'price': self.price,
            'available_places': self.available_places,
            'remaining_places': self.remaining_places,
            'start_at': self.start_at,
            'end_at': self.end_at,
            'image': self.image,
            'active': self.active,
            'organizer_id': self.organizer_id,
            'created_at': json_dump_(self.created_at),
            'updated_at': json_dump_(self.updated_at)
        }

    @classmethod
    def find_by_name(cls, name: str, active=True):
        """ Find a event by his name in the database. """
        return cls.query.filter_by(name=name).filter_by(active=active).first()

    @classmethod
    def find_by_id(cls, _id: int, active=True):
        """ Find a event by his ID in the database. """
        return cls.query.filter_by(_id=_id).filter_by(active=active).first()

    @classmethod
    def find_for_published(cls, _id: int):
        """ Find a event by his ID to publish or unpublish in the database. """
        return cls.query.filter_by(_id=_id).first()

    @classmethod
    def find_all(cls, active=True):
        """ Find all events in the database. """
        return cls.query.filter_by(active=active).all()

    def save(self):
        """ Save new event into database. """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Delete an existing event from database. """
        db.session.delete(self)
        db.session.commit()
