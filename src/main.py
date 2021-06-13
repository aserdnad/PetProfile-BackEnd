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
from models import db, User
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
    user = User.query.filter_by(email=data['email'], user_name=['uaer_name'])
    history = History.create()

    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
