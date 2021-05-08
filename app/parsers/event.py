from flask_restful import reqparse

_help = 'Désolé, ce champ est obligatoire'
post_parser = reqparse.RequestParser()
post_parser.add_argument('name', type=str, required=True, help=_help)
post_parser.add_argument('location', type=str, required=True, help=_help)
post_parser.add_argument('description', type=str)
post_parser.add_argument('price', type=str)
post_parser.add_argument('available_places', type=int, required=True, help=_help)
post_parser.add_argument('start_at', type=str, required=True, help=_help)
post_parser.add_argument('end_at', type=str, required=True, help=_help)
post_parser.add_argument('image', type=str)
post_parser.add_argument('organizer_id', type=int, required=True, help=_help)

put_parser = post_parser.copy()
put_parser.remove_argument('organizer_id')
put_parser.add_argument('active', type=bool, required=True, help=_help)

active_parser = reqparse.RequestParser()
active_parser.add_argument('active', type=bool, required=True, help=_help)
