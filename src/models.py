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