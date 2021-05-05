from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash


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
    address = db.Column(db.String(120), nullable=False)
    contacts = db.Column(db.String(120), nullable=False)
    photo = db.Column(db.String(120), nullable=True)
    role = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(
        self,
        firstname,
        lastname,
        address,
        contacts,
        photo,
        email,
        password,
        role
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.contacts = contacts
        self.photo = photo
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role

    def json(self):
        """ Use to format the user object in json. """
        return {
            '_id': self._id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'address': self.address,
            'contacts': self.contacts,
            'photo': self.photo,
            'email': self.email,
            'role': self.role
        }

    @classmethod
    def find_by_email(cls, email: str):
        """ Find a user by his EMAIL in the database. """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int):
        """ Find a user by his ID in the database. """
        return cls.query.filter_by(_id=_id).first()

    @classmethod
    def find_all(cls):
        """ Find all user in the database. """
        return cls.query.all()

    @staticmethod
    def save(self):
        """ Save new user into database. """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def delete(self):
        """ Delete an existing user from database. """
        db.session.add(self)
        db.session.commit()
