# MYSQL
mysql_db_username = 'root'
mysql_db_password = ''
mysql_db_name = 'flask-angularjs-api’'
mysql_db_hostname = 'localhost'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{DB_USER}:{DB_PWD}@{DB_HOST}/{DB_NAME}".format(DB_USER=mysql_db_username,
 DB_PWD=mysql_db_password,
 DB_HOST=mysql_db_hostname,
 DB_NAME=mysql_db_name)

'''
	mysql is the dialect
	pymysql is the DBAPI Driver installed which i used
	to install pymysql just do : pip install pymysql

	It is always very important to specify the dialect and the driver you use for your connection
	The driver you use must be appropriate for the dialect you choose to use 
'''