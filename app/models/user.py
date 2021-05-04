from database import db


class UserModel(db.Model):
    __tablename__ = 'users'
    _id = db.Column(db.Integer, primary_key=True)

    def __init__(self):
        pass
