from flask_restful import Resource


class User(Resource):
    @classmethod
    def get(cls, _id):
        return {'_id': _id}
