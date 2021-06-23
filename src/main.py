"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, make_response
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, History, Photo_add, Pet, Calendar, Vacune
from flask_jwt_extended import create_access_token, JWTManager, jwt_required
import cloudinary.uploader as uploader

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_mapping(
    CLOUDINARY_URL=os.environ.get("CLOUDINARY_URL")
)
cloudinary.config( 
  cloud_name = "petprofile", 
  api_key = "519216389817554", 
  api_secret = "HT9brnidX5ZuTi9xk0TdgqV6fJk" 
)

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

@app.route("/history/<user_name>/<pet_name>", methods=["POST"])
def new_history(user_name, pet_name):

    try:
        image_file = request.files["file"]

        response = uploader.upload(image_file)  

        user = User.query.filter_by(user_name=user_name).one_or_none()

        pet = Pet.query.filter_by(name=pet_name).one_or_none()
        
        try:
            history = History.create(
                title=request.form.get("title"),
                public_id=response["public_id"], 
                image_url=response["secure_url"], 
                user_id=user.id, 
                pet_id=pet.id
                )
            if user is None:
                return jsonify({"msg": "No se encontro el usuario, vuelva intentar :D"}), 500
            if not isinstance(user, User):
                return jsonify({"msg": "ERROR of Matrix X_X User"}), 400
            if not isinstance(history, History):
                return jsonify({"msg": "ERROR of Matrix X_X History"}), 500

            return jsonify(history.serialize()), 201
            
        except:
            db.session.rollback()
            status_code = 400
            response_body = {
                "result": "HTTP_400_BAD_REQUEST. no title in key/value"
            }
    except Exception as error:
        status_code = 400
        return jsonify({
                "result": f"HTTP_400_BAD_REQUEST. {type(error)}{error.args}"
            })
    


@app.route("/photo_add/<user_name>/<pet_name>", methods=["POST"])
def new_photo_add(user_name, pet_name):

    try:
        image_file = request.files["file"]

        response = uploader.upload(image_file)  

        user = User.query.filter_by(user_name=user_name).one_or_none()

        pet = Pet.query.filter_by(name=pet_name).one_or_none()
        
        try:
            photo_add = Photo_add.create(
                title=request.form.get("title"),
                public_id=response["public_id"], 
                image_url=response["secure_url"], 
                user_id=user.id, 
                pet_id=pet.id
                )
            if user is None:
                return jsonify({"msg": "No se encontro el usuario, vuelva intentar :D"}), 500
            if not isinstance(user, User):
                return jsonify({"msg": "ERROR of Matrix X_X User"}), 400
            if not isinstance(photo_add, Photo_add):
                return jsonify({"msg": "ERROR of Matrix X_X Photo_add"}), 500

            return jsonify(photo_add.serialize()), 201


        except:
            db.session.rollback()
            status_code = 400
            response_body = {
                "result": "HTTP_400_BAD_REQUEST. no title in key/value"
            }
    except Exception as error:
        status_code = 400
        response_body = {
                "result": f"HTTP_400_BAD_REQUEST. {type(error)}{error.args}"
            }
    

@app.route("/vacune/<user_name>/<pet_name>", methods=["POST"])
def new_vacune(user_name, pet_name):

    try:
        image_file = request.files["file"]

        response = uploader.upload(image_file)  

        user = User.query.filter_by(user_name=user_name).one_or_none()

        pet = Pet.query.filter_by(name=pet_name).one_or_none()
        
        try:
            vacune = Vacune.create(
                title=request.form.get("title"),
                public_id=response["public_id"], 
                image_url=response["secure_url"], 
                user_id=user.id, 
                pet_id=pet.id
                )
            if user is None:
                return jsonify({"msg": "No se encontro el usuario, vuelva intentar :D"}), 500
            if not isinstance(user, User):
                return jsonify({"msg": "ERROR of Matrix X_X User"}), 400
            if not isinstance(photo_add, Photo_add):
                return jsonify({"msg": "ERROR of Matrix X_X Vacune"}), 500

            return jsonify(vacune.serialize()), 201

        except:
            db.session.rollback()
            status_code = 400
            response_body = {
                "result": "HTTP_400_BAD_REQUEST. no title in key/value"
            }
        

    except Exception as error:
        status_code = 400
        response_body = {
                "result": f"HTTP_400_BAD_REQUEST. {type(error)}{error.args}"
            }
    
    


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
        return jsonify({"msg": "ERROR of Matrix X_X Calendar"}), 500
    return jsonify(calendar.serialize()), 201

@app.route("/pet", methods=["POST"])
def pet():
    data = request.json
    user = User.query.filter_by(email=data['email']).one_or_none()
    pet = Pet.create(
        name = data.get('name'),
        race = data.get('race'),
        gender = data.get('gender'),
        age = data.get('age'),
        species = data.get('species'),
        weight = data.get('weight'),
        height = data.get('height'),
        birthday = data.get('birthday'),
        user_id = user.id
    )
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

    return jsonify(list(map(lambda x: x.serialize(), pet_list))), 201

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



@app.route("/photo/<int:id_image>", methods=["GET","DELETE"])
def image_by_id(id_image):

    image_get = Photo_add.query.get(id_image)

    if request.method == "GET":

        return jsonify(image_get.serialize())


    elif request.method == "DELETE":
        response = uploader.destroy(image_get.public_id)

        if "result" in response and response["result"] == "ok":
            db.session.delete(image_get)

            try:
                db.session.commit()

            except Exception as error:
                db.session.rollback()
                response_body = {
                    "results": f"HTTP_500_INTERNAL_SERVER_ERROR. {type(error)} {error.args}"
                }

            return jsonify({"msg": f"history {id_image} deleted"}), 204

        else:
            response_body = {
                "result": f"HTTP_404_NOT_FOUND.image not found..."
            }
            status_code = 404



@app.route("/history/<int:id_history>", methods=["GET", "DELETE"])
def history_by_id(id_history):

    history_get = History.query.get(id_history)
    
    if request.method == "GET":

        return jsonify(history_get.serialize())


    elif request.method == "DELETE":
        response = uploader.destroy(history_get.public_id)

        if "result" in response and response["result"] == "ok":
            db.session.delete(history_get)

            try:
                db.session.commit()

            except Exception as error:
                db.session.rollback()
                response_body = {
                    "results": f"HTTP_500_INTERNAL_SERVER_ERROR. {type(error)} {error.args}"
                }

            return jsonify({"msg": f"history {id_history} deleted"}), 204


        else:
            response_body = {
                "result": f"HTTP_404_NOT_FOUND. image not found..."
            }
            status_code = 404
            


@app.route("/vacune/<int:id_vacune>", methods=["GET", "DELETE"])
def vacune_by_id(id_vacune):

    vacune_get = Vacune.query.get(id_vacune)
    
    if request.method == "GET":

        return jsonify(vacune_get.serialize())


    elif request.method == "DELETE":

        response = uploader.destroy(vacune_get.public_id)

        if "result" in response and response["result"] == "ok":

            db.session.delete(vacune_get)

            try:
                db.session.commit()

            except Exception as error:
                db.session.rollback()
                response_body = {
                    "results": f"HTTP_500_INTERNAL_SERVER_ERROR. {type(error)} {error.args}"
                }

            return jsonify({"msg": f"history {id_vacune} deleted"}), 204


        else:
            response_body = {
                "result": f"HTTP_404_NOT_FOUND. image not found..."
            }
            status_code = 404

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
