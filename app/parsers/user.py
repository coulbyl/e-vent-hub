from flask_restful import reqparse

_help = 'Désolé, ce champ est obligatoire'
post_parser = reqparse.RequestParser()
post_parser.add_argument('firstname', type=str, required=True, help=_help)
post_parser.add_argument('lastname', type=str, required=True, help=_help)
post_parser.add_argument('address', type=str, required=True, help=_help)
post_parser.add_argument('contacts', type=str, required=True, help=_help)
post_parser.add_argument('photo', type=str)
post_parser.add_argument('email', type=str, required=True, help=_help)
post_parser.add_argument('password', type=str, required=True, help=_help)
post_parser.add_argument('role', type=str, required=True, help=_help)

put_parser = post_parser.copy()
put_parser.remove_argument('password')
put_parser.remove_argument('role')
