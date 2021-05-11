from db import db
from datetime import datetime
from werkzeug.security import generate_password_hash
from utils import json_dump_, generate_uuid


class OrganizerModel(db.Model):
    __tablename__ = 'organizers'

    _id = db.Column(db.Integer, primary_key=True)
    _uuid = db.Column(db.String(11), unique=True, default=f"or_{generate_uuid()}")
    name = db.Column(db.String(80), unique=True, nullable=False)
    contacts = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    photo = db.Column(db.String(120))
    active = db.Column(db.Boolean, default=True, nullable=False)
    events = db.relationship('EventModel', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    def __init__(self, name, contacts, email, password, photo):
        self.name = name
        self.contacts = contacts
        self.email = email
        self.password = generate_password_hash(password)
        self.photo = photo

    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'contacts': self.contacts,
            'email': self.email,
            'photo': self.photo,
            'active': self.active,
            'events': [event.json() for event in self.events],
            'created_at': json_dump_(self.created_at),
            'updated_at': json_dump_(self.updated_at),
        }

    @classmethod
    def find_by_email(cls, email: str, active=True):
        """ Find a organizer by his EMAIL in the database. """
        return cls.query.filter_by(email=email).filter_by(active=active).first()

    @classmethod
    def find_by_id(cls, _id: int, active=True):
        return cls.query.filter_by(_id=_id).filter_by(active=active).first()

    @classmethod
    def find_by_uuid(cls, _uuid: int, active=True):
        return cls.query.filter_by(_uuid=_uuid).filter_by(active=active).first()

    @classmethod
    def find_all(cls, active=True):
        """ Find all organizerd in the database. """
        return cls.query.filter_by(active=active).all()

    def save(self):
        """ Save new organizer into database. """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Delete an existing organizer from database. """
        db.session.delete(self)
        db.session.commit()
