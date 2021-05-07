from app import app
from db import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

db.init_app(app)

if __name__ == '__main__':
    manager.run()
