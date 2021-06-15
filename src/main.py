"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, History, Photo_add, Pet
from flask_jwt_extended import create_access_token, JWTManager
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route("/sign-up", methods=["POST"])
def sign_up():
    data = request.json
    user = User.create(email=data.get('email'), 
    password=data.get('password'),
    user_name=data.get('user_name'),
    name=data.get('name'),
    last_name=data.get('last_name'),
    phone=data.get('phone'),
    birthday=data.get('birthday'),
    country=data.get('country'),
    city=data.get('city'))
    if not isinstance(user, User):
        return jsonify({"msg": "ERROR of Matrix X_X"}), 500
    return jsonify(user.serialize()), 201

    #SIGN-UP ya funcional

@app.route("/log-in", methods=["POST"])
def log_in():
    
    data = request.json
    user = User.query.filter_by(email=data['email']).one_or_none()
    if user is None: 
        return jsonify({"msg": "Vuelva insertar usuario, Gracias :D"}), 404
    if not user.check_password(data.get('password')):
        return jsonify({"msg": "Password incorrecto X_x"}), 400
    token = create_access_token(identity=user.id)
    return jsonify({
        "user": user.serialize(),
        "token": token
    }), 200

@app.route("/history", methods=["POST"])
def history():
    data = request.json
    user = User.query.filter_by(email=data['email']).one_or_none()
    pet = Pet.query.filter_by(name=data['name']).one_or_none()
    history = History.create(history=data.get('history'), vacune=data.get('vacune'), user_id=user.id, pet_id=pet.id)
    if user is None:
        return jsonify({"msg": "No se encontro el usuario, vuelva intentar :D"}), 500
    if not isinstance(user, User):
        return jsonify({"msg": "ERROR of Matrix X_X User"}), 500
    if not isinstance(history, History):
        return jsonify({"msg": "ERROR of Matrix X_X History"}), 500
    return jsonify(history.serialize()), 201
    
@app.route("/photo_add", methods=["POST"])
def photo_add_user():
    data = request.json
    user = User.query.filter_by(email=data['email']).one_or_none()
    pet = Pet.query.filter_by(name=data['name']).one_or_none()
    photo_add = Photo_add.create(images=data.get('images'), user_id=user.id, pet_id=pet.id)
    if user is None:
        return jsonify({"msg": "No se encontro el usuario, vuelva intentar :D"}), 500
    if not isinstance(user, User):
        return jsonify({"msg": "ERROR of Matrix X_X User"}), 500
    if not isinstance(photo_add, Photo_add):
        return jsonify({"msg": "ERROR of Matrix X_X Photo_add"}), 500
    return jsonify(photo_add.serialize()), 201

@app.route("/pet", methods=["POST"])
def pet():
    data = request.json
    user = User.query.filter_by(email=data['email']).one_or_none()
    pet = Pet.create(name = data.get('name'),
        race = data.get('race'),
        gender = data.get('gender'),
        age = data.get('age'),
        species = data.get('species'),
        weight = data.get('weight'),
        height = data.get('height'),
        birthday = data.get('birthday'),
        user_id = user.id)
    if user is None:
        return jsonify({"msg": "No se encontro el usuario, vuelva intentar :D"}), 500
    if not isinstance(user, User):
        return jsonify({"msg": "ERROR of Matrix X_X User"}), 500
    return jsonify(pet.serialize()), 201


@app.route("/history/pet/<name>", methods=["GET"])
def history_get(name):

    pet = Pet.query.filter_by(name=name).one_or_none()
    history = History.query.filter(History.pet_id==pet.id)
    history_list = history.all()

    history_get_id = list(map(lambda x: x.id, history_list))

    history_get_list = list(map(lambda n: History.query.get(n), history_get_id))

    return jsonify(list(map(lambda x: x.serialize(), history_get_list))), 201

@app.route("/image/pet/<name>", methods=["GET"])
def image_get(name):

    pet = Pet.query.filter_by(name=name).one_or_none()
    images = Photo_add.query.filter(Photo_add.pet_id==pet.id)
    images_list = images.all()

    images_get_id = list(map(lambda x: x.id, images_list))

    images_get_list = list(map(lambda n: Photo_add.query.get(n), images_get_id))

    return jsonify(list(map(lambda x: x.serialize(), images_get_list))), 201



    return jsonify(list(map(lambda x: x.serialize(), images_get_list))), 201

    

    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
