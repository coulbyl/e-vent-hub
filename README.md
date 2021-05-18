# E-vent Hub REST Api

Api to manage events.

## Implementation

This project is implemented using Flask, Flask-RESTful, Flask-JWT-Extended, Flask-SQLALchemy, and Flask-Migrate.

Mysql database used by default.

## Locally Installation

```
[comment]: <> (install virtual environment.)

    py -m venv .venv

[comment]: <> (Activate venv on windows with git bash or cmd  | remove "source" for cmd.)

    source .venv\\Scripts\\activate

[comment]: <> (Install all packages from the requirements file.)
    pip install -r requirements.txt

[comment]: <> (Run the migrations and seeder.)
    py manage.py db upgrade
    py manage.py admin_seeder

[comment]: <> (Run the app.)
    flask run
```

## API Routes

```
[POST]
/user/register
/user/login
/organizer/register
/organizer/login
/event/store
/admin/register
/admin/login

[GET, PUT, DELETE]
/users
/organizers
/admins
/events
/events/unpublished
/events/unauthorized

/user/<int:_id>
/user/password-reset/<int:_id>
/user/favourite-event/<int:user_id>/<int:event_id>

/organizer/<int:_id>
/organizer/password-reset/<int:_id>

/event/<int:_id>
/event/publication/<int:_id>
/event/authorization/<int:_id>
/event/participant/<int:event_id>/<int:user_id>

/admin/<int:_id>
/admin/password-reset/<int:_id>
/admin/role/<int:_id>
/user/activation/<int:_id>
/organizer/activation/<int:_id>

/logout [DELETE]
/upload/<string:filename>/<string:folder> [GET, folder -> client | event | organizer]
/token/refresh [GET]
```
