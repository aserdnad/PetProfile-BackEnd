from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    user_name = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(40), unique=True, nullable=False)
    last_name = db.Column(db.String(40), unique=True, nullable=False)
    phone = db.Column(db.String(12), unique=True, nullable=False)
    birthday = db.Column(db.String(11), unique=True, nullable=False)
    country = db.Column(db.String(40), unique=True, nullable=False)
    city = db.Column(db.String(40), unique=True, nullable=False)
    sal = db.Column(db.String(40), nullable=False)
    hashed_password = db.Column(db.String(240), nullable=False)
    
    def __init__(self, **kwargs):
        print(kwargs)
        self.email = kwargs.get('email')
        self.user_name = kwargs.get("user_name")
        self.name = kwargs.get("name")
        self.last_name = kwargs.get("last_name")
        self.phone = kwargs.get("phone")
        self.birthday = kwargs.get("birthday")
        self.country = kwargs.get("country")
        self.city = kwargs.get("city")
        self.sal = os.urandom(16).hex()
        self.set_password(kwargs.get('password'))

    @classmethod
    def create(cls, **kwargs):
        user = cls(**kwargs)
        db.session.add(user)
        try: 
            db.session.commit()
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return False
        return user

    def set_password(self, password):
        print(generate_password_hash(
            f"{password}{self.sal}"
        ))
        self.hashed_password = generate_password_hash(
            f"{password}{self.sal}"
        )

    def check_password(self, password):
        return check_password_hash(
            self.hashed_password,
            f"{password}{self.sal}"
        )

    def __repr__(self):
        return '<User %r>' % self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "user_name": self.user_name,
            "name": self.name,
            "last_name": self.last_name,
            "phone": self.phone,
            "birthday": self.birthday,
            "country": self.country,
            "city": self.city
            # do not serialize the password, its a security breach
        }
class History(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    history = db.Column(db.String(40),unique=True,nullable=False)
    vacune = db.Column(db.String(40),unique=True,nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))

    user = db.relationship('User',lazy=True)

    def __init__(self,**kwargs):
        self.history = kwargs.get('history')
        self.vacune = kwargs.get('vacune')
        self.user_id = kwargs.get('user_id')

    @classmethod
    def create(cls, **kwargs):
        history = cls(**kwargs)
        db.session.add(history)
        try: 
            db.session.commit()
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return False
        return history
    
    def __repr__(self):
        return '<History %r>' % self.history

    def serialize(self):
        return {
        "id": self.id,
        "history": self.history,
        "vacune": self.vacune,
        "user_id": self.user_id
        }


class Photo_add(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    images = db.Column(db.String(40),unique=True,nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))

    user = db.relationship('User',lazy=True)

    def __init__(self,**kwargs):
        self.images = kwargs.get('images')
        self.user_id = kwargs.get('user_id')

    @classmethod
    def create(cls, **kwargs):
        photo_add = cls(**kwargs)
        db.session.add(photo_add)
        try: 
            db.session.commit()
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return False
        return photo_add

    def __repr__(self):
        return '<Photo_add %r>' % self.images

    def serialize(self):
        return {
        "id": self.id,
        "images": self.images,
        "user_id": self.user_id
        }


class Pet(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40),unique=True,nullable=False)
    race = db.Column(db.String(40),unique=True,nullable=False)
    gender = db.Column(db.String(40),unique=True,nullable=False)
    age = db.Column(db.Integer(),unique=True,nullable=False)
    species = db.Column(db.String(40),unique=True,nullable=False)
    weight = db.Column(db.Integer(),unique=True,nullable=False)
    height = db.Column(db.Integer(),unique=True,nullable=False)
    birthday = db.Column(db.Integer(),unique=True,nullable=False)
    photo_add_id = db.Column(db.Integer(), db.ForeignKey(Photo_add.id))
    history_id = db.Column(db.Integer(), db.ForeignKey(History.id))
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))

    user = db.relationship('User',lazy=True)
    photo = db.relationship('Photo_add',lazy=True)
    history = db.relationship('History',lazy=True)

    def __init__(self,**kwargs):
        self.name = kwargs.get('name')
        self.race = kwargs.get('race')
        self.gender = kwargs.get('gender')
        self.age = kwargs.get('age')
        self.species = kwargs.get('species')
        self.weight = kwargs.get('weight')
        self.height = kwargs.get('height')
        self.birthday = kwargs.get('birthday')
        self.photo_add_id = kwargs.get('photo_add_id')
        self.history_id = kwargs.get('history_id')
        self.user_id = kwargs.get('user_id')

    @classmethod
    def create(cls, **kwargs):
        pet = cls(**kwargs)
        db.session.add(pet)
        try: 
            db.session.commit()
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return False
        return pet

    def __repr__(self):
        return '<Pet %r>' % self.name

    def serialize(self):
        return {
        "id": self.id,
        "name": self.name,
        "race": self.race,
        "gender": self.gender,
        "age": self.age,
        "species": self.species,
        "weight": self.weight,
        "height": self.height,
        "birthday": self.birthday,
        "photo_add_id": list(map(lambda relation: relation.photo_add.images, self.photo_add_id)),
        "history_id": list(map(lambda relation: relation.history.serialize(), self.history_id)),
        "user_id": self.user_id
        }
