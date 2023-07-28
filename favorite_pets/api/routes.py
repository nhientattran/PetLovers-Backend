from flask import Blueprint, request, jsonify
from favorite_pets.helpers import token_required
from favorite_pets.models import db, Pet, pet_schema, pets_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some': 'value'}

# Create Pet Endpoint
@api.route('/pets', methods = ['POST'])
@token_required
def create_pet(our_user):
    name = request.json['name']
    photos = request.json['photos']
    description = request.json['description']
    breeds = request.json['breeds']
    gender = request.json['gender']
    age = request.json['age']
    size = request.json['size']
    distance = request.json['distance']
    contact = request.json['contact']
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    pet = Pet(name, photos, description, breeds, gender, age, size, distance, contact, user_token)
    
    db.session.add(pet)
    db.session.commit()

    response = pet_schema.dump(pet)

    return jsonify(response)

# Read 1 Single Pet Endpoint
@api.route('/pets/<id>', methods = ['GET'])
@token_required
def get_pet(our_user, id):
    if id:
        pet = Pet.query.get(id)
        response = pet_schema.dump(pet)
        return jsonify(response)
    else:
        return jsonify({'message': 'ID is missing'}), 401
    
# Read all the Drones
@api.route('/pets', methods = ['GET'])
@token_required
def get_pets(our_user):
    token = our_user.token
    pets = Pet.query.filter_by(user_token = token).all()
    response = pets_schema.dump(pets)
    return jsonify(response)

# Update 1 Pet by ID
@api.route('/pets/<id>', methods = ['PUT'])
@token_required
def update_pet(our_user, id):
    pet = Pet.query.get(id)

    pet.name = request.json['name']
    pet.photos = request.json['photos']
    pet.description = request.json['description']
    pet.breeds = request.json['breeds']
    pet.gender = request.json['gender']
    pet.age = request.json['age']
    pet.size = request.json['size']
    pet.distance = request.json['distance']
    pet.contact = request.json['contact']
    pet.user_token = our_user.token

    db.session.commit()

    response = pet_schema.dump(pet)

    return jsonify(response)

# Delete 1 Drone by ID
@api.route('/pets/<id>', methods = ['DELETE'])
@token_required
def delete_pet(our_user, id):
    pet = Pet.query.get(id)
    db.session.delete(pet)
    db.session.commit()

    response = pet_schema.dump(pet)

    return jsonify(response)