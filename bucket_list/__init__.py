from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key = 'development key'

# use with sqlalchemy and pymysql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bucketlist'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8889/bucketlist'

# using flask-mysql wo sqlalchemy
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 8889
app.config['MYSQL_DATABASE_DB'] = 'bucketlist'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'

mysql = MySQL()
mysql.init_app(app)

# use with sqlalchemy and pymysql
# from bucket_list.models import db
# db.init_app(app)

import bucket_list.routes