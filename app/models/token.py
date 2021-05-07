from db import db
from datetime import datetime
from utils import json_dump_


class TokenBlockList(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, jti):
        self.jti = jti

    def json(self):
        return {'_id': self._id, 'jti': self.jti, 'created_at': json_dump_(self.created_at)}

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_jti(cls, jti):
        return cls.query.filter_by(jti=jti).scalar()
