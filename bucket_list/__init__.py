from flask import Flask

app = Flask(__name__)

app.secret_key = 'development key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bucketlist'

from bucket_list.models import db
db.init_app(app)

import bucket_list.routes