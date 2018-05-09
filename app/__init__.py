from flask import Flask

def create_app(config_filename):
    app = Flask(__name__, static_folder='templates/static') # instantiate flask application
    app.config.from_object(config_filename)
            
    #Init Flask-SQLAlchemy
    from app.models import db
    db.init_app(app)	# binds the application to the db

from app.controller import users
 app.register_blueprint(users, url_prefix='/api/v1/users')	# register blueprint
 
from flask import render_template, send_from_directory 

@app.route('/&lt;path:filename&gt;')	# in order words /<path:filename>
def file(filename):
	from os import path
	return send_from_directory(path.join(app.root_path, 'templates'), filename)	# send file with name 'filename' from its current directory to the specified directory

@app.route('/')
def index():
	return render_template('index.html')
 
return app