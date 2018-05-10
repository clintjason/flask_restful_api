from flask import Flask, render_template, send_from_directory
from app.models import db
from app.controller import users

def create_app(config_filename):
    app = Flask(__name__, static_folder='templates/static') # instantiate flask application
    app.config.from_object(config_filename)	# load db configurations : however will load only the uppercase attributes of the module or class
            
    #Init Flask-SQLAlchemy
    db.init_app(app)	# binds the application to the db

    app.register_blueprint(users, url_prefix='/api/v1/users')	# register blueprint

    @app.route('/&lt;path:filename&gt;')	# in order words /<path:filename>
    def file(filename):
    	from os import path
    	return send_from_directory(path.join(app.root_path, 'templates'), filename)	# send file with name 'filename' from its current directory to the specified directory

	@app.route('/')
	def index():
		return render_template('index.html')

	return app