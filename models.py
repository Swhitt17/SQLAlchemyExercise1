from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG_URL = 'https://en.m.wikipedia.org/wiki/File:Sample_User_Icon.png'
#Models below
    
class User(db.Model):
    __tablename__= 'users'

    id =  db.Column(db.Integer,
                 primary_key=True,
                 autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMG_URL)

    @property
    def full_name(self):
        """Gives full name of user"""
        return f"{self.first_name} {self.last_name}"


def connect_db(app):
    db.app = app
    db.init_app(app)
