from app.resources.user import User

ROUTES = [
    {'resource': User, 'endpoint': '/user/<int:_id>'}
]
