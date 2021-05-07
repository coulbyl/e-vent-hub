from db import db
from datetime import datetime
from werkzeug.security import generate_password_hash
from utils import json_dump_

user_events = db.Table(
    'user_events',
    db.Column(
        'user_id', db.Integer, db.ForeignKey('users._id'),
        primary_key=True),
    db.Column(
        'event_id', db.Integer, db.ForeignKey('events._id'),
        primary_key=True)
)


class UserModel(db.Model):
    """ 
    User model class to easily manage user data. 

    Note -> The user can have only one of the following roles: [superuser, admin, organizer, client].
    """
    __tablename__ = 'users'

    _id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    contacts = db.Column(db.String(120), nullable=False)
    photo = db.Column(db.String(120))
    user_events = db.relationship(
        'EventModel', secondary=user_events,
        lazy='subquery',  backref=db.backref('users', lazy=True))
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, firstname, lastname, email, password, contacts, photo):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = generate_password_hash(password)
        self.contacts = contacts
        self.photo = photo

    def json(self):
        """ Use to format the user object in json. """
        return {
            '_id': self._id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'contacts': self.contacts,
            'photo': self.photo,
            'user_events': self.user_events,
            'active': self.active,
            'created_at': json_dump_(self.created_at)
        }

    @classmethod
    def find_by_email(cls, email: str, active=True):
        """ Find a user by his EMAIL in the database. """
        return cls.query.filter_by(email=email).filter_by(active=active).first()

    @classmethod
    def find_by_id(cls, _id: int, active=True):
        """ Find a user by his ID in the database. """
        return cls.query.filter_by(_id=_id).filter_by(active=active).first()

    @classmethod
    def find_all(cls, active=True):
        """ Find all user in the database. """
        return cls.query.filter_by(active=active).all()

    def save(self):
        """ Save new user into database. """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Delete an existing user from database. """
        db.session.delete(self)
        db.session.commit()

    def add_favorite(self, Event):
        event = Event()
        user = self()
        user.user_events.append(event)
        db.session.add(user)
        db.session.commit()

    def remove_favorite(self, Event):
        pass
