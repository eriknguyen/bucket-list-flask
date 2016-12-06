from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(200))

    def __init__(self, name, username, password):
        self.name = name
        self.email = username
        self.set_password(password)

    def set_password(self, _password):
        self.password = generate_password_hash(_password)

    def check_password(self, _password):
        return check_password_hash(self.password, _password)

    def print_user(self):
        print ("User: ", self.name, " - ", self.email)