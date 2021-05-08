from app.resources.user import (
    User, UserRegister, UserList, UserPasswordReset,
    UserLogin, Logout, TokenRefresh, UserFavouriteEvent
)

from app.resources.organizer import (
    Organizer, OrganizerRegister, OrganizerList, OrganizerPasswordReset,
    OrganizerLogin
)

from app.resources.event import (
    Event, EventStore, EventPublishedList, EventUnpublishedList, EventPublication,
    EventParticipant
)

from app.resources.admin import (
    Admin, AdminRegister, AdminList, AdminLogin, AdminPasswordReset
)

ROUTES = [
    # User
    {'resource': User, 'endpoint': '/user/<int:_id>'},
    {'resource': UserRegister, 'endpoint': '/register'},
    {'resource': UserList, 'endpoint': '/users'},
    {'resource': UserLogin, 'endpoint': '/login'},
    {'resource': UserPasswordReset, 'endpoint': '/password-reset/<int:_id>'},
    {
        'resource': UserFavouriteEvent,
        'endpoint': '/user/favourite-event/<int:user_id>/<int:event_id>'
    },

    # Organizer
    {'resource': Organizer, 'endpoint': '/organizer/<int:_id>'},
    {'resource': OrganizerRegister, 'endpoint': '/organizer/register'},
    {'resource': OrganizerList, 'endpoint': '/organizers'},
    {'resource': OrganizerLogin, 'endpoint': '/organizer/login'},
    {
        'resource': OrganizerPasswordReset,
        'endpoint': '/organizer/password-reset/<int:_id>'
    },

    # Event
    {'resource': EventStore, 'endpoint': '/event/store'},
    {'resource': Event, 'endpoint': '/event/<int:_id>'},
    {'resource': EventPublishedList, 'endpoint': '/events'},
    {'resource': EventPublication, 'endpoint': '/event/publication/<int:_id>'},
    {'resource': EventUnpublishedList, 'endpoint': '/events/unpublished'},
    {
        'resource': EventParticipant,
        'endpoint': '/event/participant/<int:event_id>/<int:user_id>'
    },

    # Admin
    {'resource': Admin, 'endpoint': '/admin/<int:_id>'},
    {'resource': AdminRegister, 'endpoint': '/admin/register'},
    {'resource': AdminList, 'endpoint': '/admins'},
    {'resource': AdminLogin, 'endpoint': '/admin/login'},
    {'resource': AdminPasswordReset, 'endpoint': '/admin/password-reset/<int:_id>'},

    # Global
    {'resource': Logout, 'endpoint': '/logout'},
    {'resource': TokenRefresh, 'endpoint': '/token/refresh'},
]
