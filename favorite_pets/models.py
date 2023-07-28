from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import uuid 
from datetime import datetime 


# Adding Flask Security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import Secrets Module
import secrets 

# Import for LoginManager & UserMixin 
# help us login our users & store their credentials 
from flask_login import UserMixin, LoginManager

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) 


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    username = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    pet = db.relationship('Pet', backref = 'owner', lazy = True)

    def __init__(self, email, username, password, first_name = '', last_name = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token()
        self.username = username 


    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self):
        return secrets.token_hex(24)
    

    def __repr__(self):
        return f"User {self.email} has been added to the database! Woohoo!"
    

class Pet(db.Model): 
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String)
    photos = db.Column(db.String, nullable = True)
    description = db.Column(db.String)
    breeds = db.Column(db.String)
    gender = db.Column(db.String)
    age = db.Column(db.String)
    size = db.Column(db.String)
    distance = db.Column(db.String)
    contact = db.Column(db.String)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, photos, description, breeds, gender, age, size, distance, contact, user_token):
        self.id = self.set_id()
        self.name = name
        self.photos = photos
        self.description = description
        self.breed = breeds
        self.gender = gender
        self.age = age
        self.size = size
        self.distance = distance
        self.contact = contact
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"Pet {self.name} has been added to the database! Woohoo!"
    

class PetSchema(ma.Schema): 
    class Meta:
        fields = ['id', 'name', 'photos', 'description', 'breeds', 'gender', 'age', 'size', 'distance', 'contact']
        
pet_schema = PetSchema()
pets_schema = PetSchema(many = True)


