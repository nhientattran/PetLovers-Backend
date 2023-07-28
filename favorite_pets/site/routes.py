from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from favorite_pets.forms import PetForm
from favorite_pets.models import Pet, db


site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    print('Look at this cool project')
    return render_template('index.html')

@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    petform = PetForm()

    try:
        if request.method == 'POST' and petform.validate_on_submit():
            name = petform.name.data
            photos = petform.photos.data
            description = petform.description.data
            breed = petform.breed.data
            gender = petform.gender.data
            age = petform.age.data
            size = petform.size.data
            distance = petform.distance.data
            contact = petform.contact.data
            user_token = current_user.token 

            pet = pet(name, photos, description, breed, gender, age, size, distance, contact, user_token)
            
            db.session.add(pet)
            db.session.commit()

            return redirect(url_for('site.profile'))
    except:
        raise Exception('Pet not created, please check your form and try again')
    
    user_token = current_user.token 
    pets = Pet.query.filter_by(user_token=user_token)

    return render_template('profile.html', form=petform, pets=pets)