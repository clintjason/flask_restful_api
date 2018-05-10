from flask.ext.migrate import Migrate, MigrateCommand	# in other words from flask_migrate import Migrate, MigrateCommand
from config import SQLALCHEMY_DATABASE_URI	# add this to make sure that when the config file will be imported SQLALCHEMY_DATABASE_URI will be loaded correctly
from app.models import db
from flask import Flask
from flask.ext.script import Manager  # In other words from flask_script import Manager
from app import create_app

app = create_app('config')	# load db configs and create app
migrate = Migrate(app, db)	# initialize the Migrate
manager = Manager(app)	# initializes the Manager
manager.add_command('db', MigrateCommand)	# connects the script manager to flask_migrate
 
if __name__ == '__main__':
	manager.run()	

 '''
run the following commands to perform the actual database migrations
	Python migrate.py db init			: create an initial migration repository
	Python migrate.py db Migrate        : create a db migration
	Python migrate.py db upgrade		: apply the migrations to the db
 '''