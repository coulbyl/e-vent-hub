from flask_restful import reqparse

_help = 'Désolé, ce champ est obligatoire'
post_parser = reqparse.RequestParser()
post_parser.add_argument('firstname', type=str, required=True, help=_help)
post_parser.add_argument('lastname', type=str, required=True, help=_help)
post_parser.add_argument('email', type=str, required=True, help=_help)
post_parser.add_argument('password', type=str, required=True, help=_help)
post_parser.add_argument('contacts', type=str, required=True, help=_help)
post_parser.add_argument('photo', type=str)

put_parser = post_parser.copy()
put_parser.remove_argument('password')

reset_parser = reqparse.RequestParser()
reset_parser.add_argument('old_password', type=str, required=True, help=help)
reset_parser.add_argument('new_password', type=str, required=True, help=help)
reset_parser.add_argument('confirm_password', type=str, required=True, help=help)

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True, help=help)
login_parser.add_argument('password', type=str, required=True, help=help)
