from flask.ext.migrate import Migrate, MigrateCommand
from config import SQLALCHEMY_DATABASE_URI
from app.models import db
from flask import Flask
from flask.ext.script import Manager
from app import create_app

app = create_app('config')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
 
if __name__ == '__main__':
 manager.run()

 '''
run the following commands to perform the actual database migrations
	Python migrate.py db init
	Python migrate.py db migrate
	Python migrate.py db upgrade
 '''