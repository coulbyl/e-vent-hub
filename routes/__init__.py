from app.resources.user import User, UserRegister, UserList

ROUTES = [
    {'resource': User, 'endpoint': '/user/<int:_id>'},
    {'resource': UserRegister, 'endpoint': '/user/register'},
    {'resource': UserList, 'endpoint': '/users'},
]
