from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    user_name = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(40), unique=False, nullable=False)
    last_name = db.Column(db.String(40), unique=False, nullable=False)
    phone = db.Column(db.String(12), unique=True, nullable=False)
    birthday = db.Column(db.String(11), unique=False, nullable=False)
    country = db.Column(db.String(40), unique=False, nullable=False)
    city = db.Column(db.String(40), unique=False, nullable=False)
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

    def save(self):
        
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return False

   

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

class Pet(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40),unique=False,nullable=False)
    race = db.Column(db.String(40),unique=False,nullable=False)
    gender = db.Column(db.String(40),unique=False,nullable=False)
    age = db.Column(db.String(10),unique=False,nullable=False)
    species = db.Column(db.String(40),unique=False,nullable=False)
    weight = db.Column(db.String(10),unique=False,nullable=False)
    height = db.Column(db.String(10),unique=False,nullable=False)
    birthday = db.Column(db.String(11),unique=False,nullable=False)
    
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))

    user = db.relationship('User',lazy=True)

    def __init__(self,**kwargs):
        self.name = kwargs.get('name')
        self.race = kwargs.get('race')
        self.gender = kwargs.get('gender')
        self.age = kwargs.get('age')
        self.species = kwargs.get('species')
        self.weight = kwargs.get('weight')
        self.height = kwargs.get('height')
        self.birthday = kwargs.get('birthday')
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

    
    def save(self):
        
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return False

    
    

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
        "user_id": self.user_id
        }

class History(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    history = db.Column(db.String(150),unique=False,nullable=False)
    history_key = db.Column(db.String(150),unique=True,nullable=False)
    vacune = db.Column(db.String(150),unique=False,nullable=False)
    token_vacune = db.Column(db.String(150),unique=True,nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    pet_id = db.Column(db.Integer(), db.ForeignKey(Pet.id))
    user = db.relationship('User',lazy=True)
    pet = db.relationship('Pet',lazy=True)

    def __init__(self,**kwargs):
        self.history = kwargs.get('history')
        self.history_key = kwargs.get('history_key')
        self.vacune = kwargs.get('vacune')
        self.token_vacune = kwargs.get('token_vacune')
        self.user_id = kwargs.get('user_id')
        self.pet_id = kwargs.get('pet_id')

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

    def save(self):
        
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return False
    
    def __repr__(self):
        return '<History %r>' % self.history

    def serialize(self):
        return {
        "id": self.id,
        "history": self.history,
        "history_key": self.history_key,
        "vacune": self.vacune,
        "token_vacune": self.token_vacune,
        "user_id": self.user_id,
        "pet_id": self.pet_id
        }


class Photo_add(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    images = db.Column(db.String(150),unique=False,nullable=False)
    token_image = db.Column(db.String(150),unique=True,nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    pet_id = db.Column(db.Integer(), db.ForeignKey(Pet.id))
    pet = db.relationship('Pet',lazy=True)
    user = db.relationship('User',lazy=True)

    def __init__(self,**kwargs):
        self.images = kwargs.get('images')
        self.token_image = kwargs.get('token_image')
        self.user_id = kwargs.get('user_id')
        self.pet_id = kwargs.get('pet_id')

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

    def save(self):
        
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return False

    def __repr__(self):
        return '<Photo_add %r>' % self.images

    def serialize(self):
        return {
        "id": self.id,
        "images": self.images,
        "token_image": self.token_image,
        "user_id": self.user_id,
        "pet_id": self.pet_id
        }

class Calendar(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    start = db.Column(db.String(11),unique=False,nullable=False)
    end = db.Column(db.String(11),unique=True,nullable=False)
    title = db.Column(db.String(50),unique=True,nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    pet_id = db.Column(db.Integer(), db.ForeignKey(Pet.id))
    pet = db.relationship('Pet',lazy=True)
    user = db.relationship('User',lazy=True)

    def __init__(self,**kwargs):
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')
        self.title = kwargs.get('title')
        self.user_id = kwargs.get('user_id')
        self.pet_id = kwargs.get('pet_id')

    @classmethod
    def create(cls, **kwargs):
        calendar = cls(**kwargs)
        db.session.add(calendar)
        try: 
            db.session.commit()
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return False
        return calendar

    def save(self):
        
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return False

    def __repr__(self):
        return '<Calendar %r>' % self.title

    def serialize(self):
        return {
        "id": self.id,
        "start": self.start,
        "end": self.end,
        "title": self.title,
        "user_id": self.user_id,
        "pet_id": self.pet_id
        }
