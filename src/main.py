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
from models import db, User, History, Photo_add, Pet, Calendar
from flask_jwt_extended import create_access_token, JWTManager, jwt_required
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
    history = History.create(history=data.get('history'), history_key=data.get("history_key"), vacune=data.get('vacune'), token_vacune=data.get('token_vacune'), user_id=user.id, pet_id=pet.id)
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
    photo_add = Photo_add.create(images=data.get('images'),token_image=data.get('token_image'), user_id=user.id, pet_id=pet.id)
    if user is None:
        return jsonify({"msg": "No se encontro el usuario, vuelva intentar :D"}), 500
    if not isinstance(user, User):
        return jsonify({"msg": "ERROR of Matrix X_X User"}), 500
    if not isinstance(photo_add, Photo_add):
        return jsonify({"msg": "ERROR of Matrix X_X Photo_add"}), 500
    return jsonify(photo_add.serialize()), 201

@app.route("/calendar", methods=["POST"])
def calendar_user():
    data = request.json
    user = User.query.filter_by(email=data['email']).one_or_none()
    pet = Pet.query.filter_by(name=data['name']).one_or_none()
    calendar = Calendar.create(start=data.get('start'),end=data.get('end'),title=data.get('title'), user_id=user.id, pet_id=pet.id)
    if user is None:
        return jsonify({"msg": "No se encontro el usuario, vuelva intentar :D"}), 500
    if not isinstance(user, User):
        return jsonify({"msg": "ERROR of Matrix X_X User"}), 500
    if not isinstance(calendar, Calendar):
        return jsonify({"msg": "ERROR of Matrix X_X Photo_add"}), 500
    return jsonify(calendar.serialize()), 201

@app.route("/pet", methods=["POST"])
def pet():
    data = request.json
    user = User.query.filter_by(email=data['email']).one_or_none()
    print(data.get('birthday'))
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

@app.route("/calendar/pet/<name>", methods=["GET"])
def calendar_get(name):

    pet = Pet.query.filter_by(name=name).one_or_none()
    calendar = Calendar.query.filter(Calendar.pet_id==pet.id)
    calendar_list = calendar.all()

    calendar_get_id = list(map(lambda x: x.id, calendar_list))

    calendar_get_list = list(map(lambda n: Calendar.query.get(n), calendar_get_id))

    return jsonify(list(map(lambda x: x.serialize(), calendar_get_list))), 201


@app.route("/pet/<user_name>", methods=["GET"])
def pet_get(user_name):

    user = User.query.filter_by(user_name=user_name).one_or_none()
    pet = Pet.query.filter(Pet.user_id==user.id)
    pet_list = pet.all()

    pet_get_id = list(map(lambda x: x.id, pet_list))

    pet_get_list = list(map(lambda n: Pet.query.get(n), pet_get_id))

    return jsonify(list(map(lambda x: x.serialize(), pet_get_list))), 201

@app.route("/user/<int:id_user>", methods=["GET", "PUT"])
@jwt_required()
def user_by_id(id_user):

    user = User.query.get(id_user)
    data = request.json
    if request.method == "GET":

        return jsonify(user.serialize())

    elif request.method == "PUT":
        try: 
            if 'country' in data:
                user.country = data['country']
            if 'email' in data:
                user.email = data['email']
            if 'city' in data: 
                user.city = data['city']
            if 'phone' in data:
                user.phone = data['phone']
           
        except:
            raise APIException('Some data failed', status_code=400)

        user.save()

        return jsonify(user.serialize())

@app.route("/pet/<int:id_pet>", methods=["GET", "PUT", "DELETE"])
def pet_by_id(id_pet):

    pet = Pet.query.get(id_pet)
    data = request.json
    if request.method == "GET":

        return jsonify(pet.serialize())

    elif request.method == "PUT":
        try: 
            if 'age' in data:
                pet.age = data['age']
            if 'weight' in data:
                pet.weight = data['weight']
            if 'height' in data: 
                pet.height = data['height']
           
        except:
            raise APIException('Some data failed', status_code=400)

        pet.save()

        return jsonify(pet.serialize())

    elif request.method == "DELETE":
        db.session.delete(pet)
        db.session.commit()
        
        return jsonify({"msg": f"pet {id_pet} deleted"}), 200

@app.route("/photo/<int:id_image>", methods=["GET", "PUT", "DELETE"])
def image_by_id(id_image):

    image = Photo_add.query.get(id_image)
    data = request.json
    if request.method == "GET":

        return jsonify(image.serialize())

    elif request.method == "PUT":
        try: 
            if 'images' in data:
                image.images = data['images']
            if 'token_image' in data:
                image.token_image = data['token_image']
            
           
        except:
            raise APIException('Some data failed', status_code=400)

        image.save()

        return jsonify(image.serialize())

    elif request.method == "DELETE":
        db.session.delete(image)
        db.session.commit()
        
        return jsonify({"msg": f"image {id_image} deleted"}), 200

@app.route("/history/<int:id_history>", methods=["GET", "PUT", "DELETE"])
def history_by_id(id_history):

    history_get = History.query.get(id_history)
    data = request.json
    if request.method == "GET":

        return jsonify(history_get.serialize())

    elif request.method == "PUT":
        try: 
            if 'history' in data:
                history_get.history = data['history']
            if 'vacune' in data:
                history_get.vacune = data['vacune']
            if 'history_key' in data:
                history_get.history_key = data['history_key']
            if 'token_vacune' in data:
                history_get.token_vacune = data['token_vacune']
            
           
        except:
            raise APIException('Some data failed', status_code=400)

        history_get.save()

        return jsonify(history_get.serialize())

    elif request.method == "DELETE":
        db.session.delete(history_get)
        db.session.commit()
        
        return jsonify({"msg": f"history {id_history} deleted"}), 200

@app.route("/calendar/<int:id_calendar>", methods=["GET", "PUT", "DELETE"])
def calendar_by_id(id_calendar):

    calendar_get = Calendar.query.get(id_calendar)
    data = request.json
    if request.method == "GET":

        return jsonify(calendar_get.serialize())

    elif request.method == "PUT":
        try: 
            if 'start' in data:
                calendar_get.start = data['start']
            if 'end' in data:
                calendar_get.end = data['end']
            if 'title' in data:
                calendar_get.title = data['title']
            
           
        except:
            raise APIException('Some data failed', status_code=400)

        calendar_get.save()

        return jsonify(calendar_get.serialize())

    elif request.method == "DELETE":
        db.session.delete(calendar_get)
        db.session.commit()
        
        return jsonify({"msg": f"calendar {id_calendar} deleted"}), 200






    
        
       

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
