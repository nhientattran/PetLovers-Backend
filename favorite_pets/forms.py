from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    email = StringField('email', validators= [DataRequired()])
    password = PasswordField('password', validators = [DataRequired()])
    submit_button = SubmitField()

class PetForm(FlaskForm):
    name = StringField('name')
    photos = StringField('photos')
    description = DecimalField('description')
    breeds = StringField('breeds')
    gender = StringField('gender')
    age = StringField('age')
    size = StringField('size')
    distance = StringField('distance')
    contact = DecimalField('contact')
    submit_button = SubmitField()