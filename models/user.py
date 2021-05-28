from db import db
from datetime import datetime
from werkzeug.security import generate_password_hash
from utils import json_dump_, generate_uuid

favourite_events = db.Table(
    'favourite_events',
    db.Column(
        'user_id', db.Integer, db.ForeignKey('users._id'),
        primary_key=True),
    db.Column(
        'event_id', db.Integer, db.ForeignKey('events._id'),
        primary_key=True)
)


class UserModel(db.Model):
    """ User model class to easily manage user data. """
    __tablename__ = 'users'

    _id = db.Column(db.Integer, primary_key=True)
    _uuid = db.Column(db.String(11), unique=True, default=f"us_{generate_uuid()}")
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    contacts = db.Column(db.String(120), nullable=False)
    photo = db.Column(db.String(120))

    favourite_events = db.relationship(
        'EventModel', secondary=favourite_events, lazy='subquery')

    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, firstname, lastname, email, password, contacts, photo):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = generate_password_hash(password)
        self.contacts = contacts
        self.photo = photo

    def json(self):
        from schema.event import EventSchema
        events_schema = EventSchema(many=True)

        return {
            '_id': self._id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'contacts': self.contacts,
            'photo': self.photo,
            'favourite_events': events_schema.dump(self.favourite_events),
            'active': self.active,
            'deleted': self.deleted,
            'created_at': json_dump_(self.created_at),
            'updated_at': json_dump_(self.updated_at)
        }

    @classmethod
    def find_by_email(cls, email: str, active=True):
        """ Find a user by his EMAIL in the database. """
        return cls.query.filter_by(
            email=email).filter_by(
            deleted=False).filter_by(
            active=active).first()

    @classmethod
    def find_by_id(cls, _id: int, active=True):
        """ Find a user by his ID in the database. """
        return cls.query.filter_by(
            _id=_id).filter_by(
            deleted=False).filter_by(
            active=active).first()

    @classmethod
    def find_without_active(cls, _id: int):
        """ Find a user by its ID without relying on the active property in the database."""
        return cls.query.filter_by(_id=_id).filter_by(deleted=False).first()

    @classmethod
    def find_by_uuid(cls, _uuid: int, active=True):
        return cls.query.filter_by(
            _uuid=_uuid).filter_by(
            deleted=False).filter_by(
            active=active).first()

    @classmethod
    def find_all(cls, active=True):
        """ Find all user in the database. """
        return cls.query.filter_by(active=active).filter_by(deleted=False).all()

    def save(self):
        """ Save new user into database. """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Delete an existing user from database. """
        db.session.delete(self)
        db.session.commit()

    def add_favourite(self, event):
        self.favourite_events.append(event)
        db.session.add(self)
        db.session.commit()

    def remove_favourite(self, event):
        self.favourite_events.remove(event)
        db.session.commit()
