from app import app
from db import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models.admin import AdminModel

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def admin_seeder():
    """ add first superuser in the database. """
    try:
        superuser = AdminModel(
            'event@hub',
            'contact@eventhub.com',
            'events#2021',
            '0759807218',
            'superuser'
        )
        superuser.save()
        print('superuser seeded.')
    except Exception as e:
        print(e.__str__())


db.init_app(app)

if __name__ == '__main__':
    manager.run()
