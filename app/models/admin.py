from db import db
from datetime import datetime
from werkzeug.security import generate_password_hash
from utils import json_dump_


class AdminModel(db.Model):
    """ 
    Admin model class to easily manage admin data. 

    Note -> The admin can have only one of the following roles: [superuser and admin].
    """
    __tablename__ = 'admins'

    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    contacts = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime)

    def __init__(self, username, email, password, contacts, role):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.contacts = contacts
        self.role = role

    def json(self):
        """ Use to format the admin object in json. """
        return {
            '_id': self._id,
            'username': self.username,
            'email': self.email,
            'contacts': self.contacts,
            'role': self.role,
            'active': self.active,
            'created_at': json_dump_(self.created_at),
            'updated_at': json_dump_(self.updated_at)
        }

    @classmethod
    def find_by_email(cls, email: str, active=True):
        """ Find a admin by his EMAIL in the database. """
        return cls.query.filter_by(email=email).filter_by(active=active).first()

    @classmethod
    def find_by_id(cls, _id: int, active=True):
        """ Find a admin by his ID in the database. """
        return cls.query.filter_by(_id=_id).filter_by(active=active).first()

    @classmethod
    def find_all(cls, active=True):
        """ Find all admin in the database. """
        return cls.query.filter_by(active=active).all()

    def save(self):
        """ Save new admin into database. """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Delete an existing admin from database. """
        db.session.delete(self)
        db.session.commit()
