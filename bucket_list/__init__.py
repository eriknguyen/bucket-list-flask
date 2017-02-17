from flask import Flask
from flask.ext.mysql import mysql

app = Flask(__name__)

app.secret_key = 'development key'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bucketlist'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8889/bucketlist'

from bucket_list.models import db
db.init_app(app)

import bucket_list.routes