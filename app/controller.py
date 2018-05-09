from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from app.models import db, Users, UsersSchema
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

#Initialize a Flask Blueprint,
users = Blueprint('users', __name__) #__name__ refers to the name of the current module

#Initialize the UserSchema we defined in models.py
schema = UsersSchema(strict=True)

#Initialize an API object using the Flask-RESTful API class
api = Api(users)

# Create CRUD classes using the Flask-RESTful Resource class
class CreateListUsers(Resource):
 
	def get(self):
		users_query = Users.query.all()	# returns a list of all Users 
		results = schema.dump(users_query, many=True).data
		# schema.dump will serialize the list of Users into a dictionary: many is set to True coz users_query is a collection
		return results

	def post(self):
		raw_dict = request.get_json(force=True) # this will get the json string and force is set to true to ignore the mimetype so that we don't get None as results if the mimetype is other than application/json
		try:
			schema.validate(raw_dict) # returns a dictionary of validation errors
			request_dict = raw_dict['data']['attributes'] # assign the value of raw_dict ['data']['attributes'] to request_dict
			print(raw_dict)
			user = Users(request_dict['name'], request_dict['address'], request_dict['age'], request_dict[
			'profession'], request_dict['website']) # instantiate the Users class
			user.add(user)	# inserts a user record
			# Should not return password hash
			query = Users.query.get(user.id) # assigns user object with id 'user.id' to query
			results = schema.dump(query).data	# serialize 'query' to a dictionary and returns it in 'results'
			return results, 201	# 201 is the code for resource created.

		except ValidationError as err:
			resp = jsonify({"error": err.messages})
			resp.status_code = 403
			return resp

		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp

class GetUpdateDeleteUser(Resource):

	def get(self, id):
		user_query = Users.query.get_or_404(id) # get user by id or else raise a 404 error
		result = schema.dump(user_query).data	# serialize user object into a dictionary
		return result   # return resutls

	def patch(self, id):
		user = Users.query.get_or_404(id)  # get user by id or raise a 404 error
		raw_dict = request.get_json(force=True)		# get json results as a string from the request obj no matter the mimetype

		try:
			schema.validate(raw_dict)	# validate the inputs and returns a dictionary of validation errors accessible using ValidationError.messages
			request_dict = raw_dict['data']['attributes']
			for key, value in request_dict.items():
				setattr(user, key, value)
				user.update()	# save new changes
				return self.get(id)

		except ValidationError as err:
			resp = jsonify({"error": err.messages}) #jsonify() function in flask returns a flask.Response() object that already has the appropriate content-type header 'application/json' for use with json responses
			resp.status_code = 401  # status codes have default values for various requests but sometimes these has to be overridden like in this case
			return resp

		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 401	#401 refers to unauthorized. For the request to be valid there is need for authentication
			return resp

	def delete(self, id):
		user = Users.query.get_or_404(id)

		try:
			delete = user.delete(user)
			response = make_response()
			response.status_code = 204	# means the response must not need a body
			return response

		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 401
			return resp

#Map classes to API enpoints
api.add_resource(CreateListUsers, '.json')
api.add_resource(GetUpdateDeleteUser, '/<int:id>.json')