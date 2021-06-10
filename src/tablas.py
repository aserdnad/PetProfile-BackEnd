class History(db.Model):
  id = db.column(db.Integer,primary_key=True)
  history = db.column(db.String(40),unique=True,nullable=False)
  vacune = db.column(db.String(40),unique=True,nullable=False)
  user_id = db.column(db.Integer(), db.ForeignKey(User.id))

  user = db.relationship('User',lazy=True)

  def __init__(self,**kwargs):
    self.history = kwargs.get('history')
    self.vacune = kwargs.get('vacune')
    self.user_id = kwargs.get('user_id')
  
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
  id = db.column(db.Integer,primary_key=True)
  images = db.column(db.String(40),unique=True,nullable=False)
  user_id = db.column(db.Interger(), db.ForeignKey(User.id))

  user = db.relationship('User',lazy=True)

  def __init__(self,**kwargs):
    self.images = kwargs.get('images')
    self.user_id = kwargs.get('user_id')

  def __repr__(self):
    return '<Photo_add %r>' % self.images

  def serialize(self):
    return {
      "id": self.id,
      "images": self.images,
      "user_id": self.user_id
    }


class Pet(db.Model):
  id = db.column(db.Integer,primary_key=True)
  name = db.column(db.String(40),unique=True,nullable=False)
  race = db.column(db.String(40),unique=True,nullable=False)
  gender = db.column(db.String(40),unique=True,nullable=False)
  age = db.column(db.Integer(),unique=True,nullable=False)
  species = db.column(db.String(40),unique=True,nullable=False)
  weight = db.column(db.Integer(),unique=True,nullable=False)
  height = db.column(db.Integer(),unique=True,nullable=False)
  birthday = db.column(db.Integer(),unique=True,nullable=False)
  photo_add_id = db.column(db.Interger(), db.ForeignKey(Photo_add.id))
  history_id = db.column(db.Interger(), db.ForeignKey(History.id))
  user_id = db.column(db.Interger(), db.ForeignKey(User.id))

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

  def __repr__(self):
    return '<Pet %r>' % self.name

  def serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "race": self.race
      "age": self.age,
      "species": self.species,
      "weight": self.weight,
      "height": self.height,
      "birthday": self.birthday,
      "photo_add_id": self.photo_add_id,
      "history_id": self.history_id,
      "user_id": self.user_id
      }



class Post(db.Model):
  id = db.column(db.Integer,primary_key=True)
  footer_description = db.column(db.String(40),unique=True,nullable=False)
  place = db.column(db.String(40),unique=True,nullable=False)
  date = db.column(db.Integer(),unique=True,nullable=False)
  user_id = db.column(db.Integer(), db.ForeignKey(User.id))
  pet_id = db.column(db.Integer(), db.ForeignKey(Pet.id))
  photo_add_id = db.column(db.Integer(), db.ForeignKey(Photo_add.id))
  # interaction_id = db.column(db.Integer(), db.ForeignKey(Interaction.id))

  user = db.relationship('User',lazy=True)
  photo = db.relationship('Photo_add',lazy=True)
  pet = db.relationship('Pet',lazy=True)
  # interaction = db.relationship('Interaction',lazy=True)

  def __init__(self,**kwargs):
    self.footer_description = kwargs.get('footer_description')
    self.place = kwargs.get('place')
    self.date = kwargs.get('date')
    self.user_id = kwargs.get('user_id')
    self.pet_id = kwargs.get('pet_id')
    self.photo_add_id = kwargs.get('photo_add_id')
    # self.interaction_id = kwargs.get('interaction_id')

  def __repr__(self):
    return '<Post %r>' % self.footer_description#
      
  def serialize(self):
    return {
      "id": self.id,
      "footer_description": self.footer_description,
      "place": self.place
      "date": self.date,
      "user_id": self.user_id,
      "pet_id": self.pet_id,
      "photo_add_id": self.photo_add_id
      # "interaction_id": self.interaction_id
      }

    

class Guess(db.Model):
  id = db.column(db.Integer,primary_key=True)
  pet_id = db.column(db.Integer(), db.ForeignKey(Pet.id))

  pet = db.relationship('Pet',lazy=True)

  def __init__(self,**kwargs):
    self.pet_id = kwargs.get('pet_id')

  def __repr__(self):
    return '<Guess %r>' % self.pet_id

  def serialize(self):
    return {
      "id": self.id,
      "pet_id": self.pet_id
    }



# class Interaction(db.Model):
#   id = db.column(db.Integer,primary_key=True)
#   like = db.column(db.Integer(),unique=True,nullable=False)
#   comment = db.column(db.String(40),unique=True,nullable=False)
#   post_id = db.column(db.Integer(), db.ForeignKey(Post.id))
#   guess_id = db.column(db.Integer(), db.ForeignKey(Post.id))

#   post = db.relationship('User',lazy=True)
#   guess = db.relationship('Guess',lazy=True)

#   def __init__(self,**kwargs):
#     self.like = kwargs.get('like')
#     self.comment = kwargs.get('comment')
#     self.post_id = kwargs.get('post_id')
#     self.guess_id = kwargs.get('guess_id')

#   def __repr__(self):
#     return '<Interaction %r>' % self.like
  
#   def serialize(self):
#     return {
#       "id": self.id,
#       "like": self.like,
#       "comment": self.comment,
#       "post_id": self.post_id,
#       "guess_id": self.guess_id
#     }
