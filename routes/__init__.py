from app.resources.user import (
    User, UserRegister, UserList, UserPasswordReset,
    UserLogin, Logout, TokenRefresh, UserFavouriteEvent, UserActivation
)

from app.resources.organizer import (
    Organizer, OrganizerActivation, OrganizerRegister, OrganizerList,
    OrganizerPasswordReset, OrganizerLogin
)

from app.resources.event import (
    Event, EventStore, EventPublishedList, EventUnpublishedList, EventPublication,
    EventParticipant, EventAuthorization, EventUnauthorizedList
)

from app.resources.admin import (
    Admin, AdminRegister, AdminList, AdminLogin,
    AdminPasswordReset, AdminRole
)

ROUTES = [
    # User
    {'resource': User, 'endpoint': '/user/<int:_id>'},
    {'resource': UserRegister, 'endpoint': '/user/register'},
    {'resource': UserList, 'endpoint': '/users'},
    {'resource': UserLogin, 'endpoint': '/user/login'},
    {'resource': UserPasswordReset, 'endpoint': '/user/password-reset/<int:_id>'},
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
    {'resource': EventAuthorization, 'endpoint': '/event/authorization/<int:_id>'},
    {'resource': EventUnauthorizedList, 'endpoint': '/events/unauthorized'},
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
    {'resource': AdminRole, 'endpoint': '/admin/role/<int:_id>'},
    {'resource': UserActivation, 'endpoint': '/public/activation/<int:_id>'},
    {'resource': OrganizerActivation, 'endpoint': '/organizer/activation/<int:_id>'},

    # Global
    {'resource': Logout, 'endpoint': '/logout'},
    {'resource': TokenRefresh, 'endpoint': '/token/refresh'},
]
