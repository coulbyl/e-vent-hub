from app.resources.user import (
    User, UserRegister, UserList, PasswordReset,
    UserLogin, UserLogout, TokenRefresh
)

from app.resources.organizer import (
    Organizer, OrganizerRegister, OrganizerList, OrganizerPasswordReset,
    OrganizerLogin
)

from app.resources.event import (
    Event, EventStore, EventPublishedList, EventUnpublishedList, EventPublication
)

ROUTES = [
    {'resource': User, 'endpoint': '/user/<int:_id>'},
    {'resource': UserRegister, 'endpoint': '/register'},
    {'resource': UserList, 'endpoint': '/users'},
    {'resource': UserLogin, 'endpoint': '/login'},
    {'resource': UserLogout, 'endpoint': '/logout'},
    {'resource': PasswordReset, 'endpoint': '/password-reset/<int:_id>'},
    {'resource': TokenRefresh, 'endpoint': '/token/refresh'},
    {'resource': Organizer, 'endpoint': '/organizer/<int:_id>'},
    {'resource': OrganizerRegister, 'endpoint': '/organizer/register'},
    {'resource': OrganizerList, 'endpoint': '/organizers'},
    {'resource': OrganizerLogin, 'endpoint': '/organizer/login'},
    {
        'resource': OrganizerPasswordReset,
        'endpoint': '/organizer/password-reset/<int:_id>'
    },
    {'resource': EventStore, 'endpoint': '/event/store'},
    {'resource': Event, 'endpoint': '/event/<int:_id>'},
    {'resource': EventPublishedList, 'endpoint': '/events'},
    {'resource': EventPublication, 'endpoint': '/event/publication/<int:_id>'},
    {'resource': EventUnpublishedList, 'endpoint': '/events/unpublished'},
]
