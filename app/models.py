from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()	# instantiate SQLAlchemy

class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(250), unique=True, nullable=False)
	address = db.Column(db.Text, nullable=False)
	age = db.Column(db.Integer, nullable=False)
	profession = db.Column(db.String(250), nullable=False)
	website = db.Column(db.String(250), nullable=False)

	def __init__(self, name, address, age, profession, website):
		self.name = name
		self.address = address
		self.age = age
		self.profession = profession
		self.website = website
 
	def add(self, resource):
		db.session.add(resource)
		return db.session.commit()

	def update(self):
		return db.session.commit()

	def delete(self, resource):
		db.session.delete(resource)
		return db.session.commit()

class UsersSchema(Schema):
	not_blank = validate.Length(min=1, error='Field cannot be blank')
	# add validate=not_blank in required fields
	id = fields.Integer(dump_only=True) 	# dump_only = True indicates that the field should be skipped during deserialization
	name = fields.String(validate=not_blank)
	address = fields.String(validate=not_blank)
	age = fields.Integer(required=True)
	profession = fields.String(validate=not_blank)
	website = fields.String(validate=not_blank)

	# self links
	def get_top_level_links(self, data, many):	# method to get the top level links object in our response
		if many:	# any=True if the objact is a collection and false otherwise
			self_link = "/users"	# self_url specifies the url to the resource
		else:
			self_link = "/users/{}".format(data['id'])
		return {'self': self_link}	# 
		#The below type object is a resource identifier object as per http://jsonapi.org/format/#document-resource-identifier-objects
	class Meta:
		type_ = 'users'	# required 
		#strict = True : we must usually add strick = True by default


	