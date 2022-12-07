from __init__ import db
import enum
from sqlalchemy.sql import func
from flask_login import UserMixin

class Level(enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    
class PromptType(enum.Enum):
    EMAIL = "EMAIL"
    NOTIFICATION = "NOTIFICATION"

class ActorType(enum.Enum):
    GIVER = "GIVER"
    RECEIVER = "RECEIVER"
    
# an auxiliary table: only foreign keys; created without association model class. 
# act_actors = db.Table('act_actors',
#                    db.Column('act_id', db.Integer, db.ForeignKey('gratitudeact.id')),
#                    db.Column('giver_id', db.Integer, db.ForeignKey('actor.id')),
#                    db.Column('receiver_id', db.Integer, db.ForeignKey('actor.id'))
# )
  
# class Actactors(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     act_id =  db.Column(db.Integer, db.ForeignKey('gratitudeact.id'))
#     giver_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
#     receiver_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    
                   
class Actofkindness(db.Model):
    __name__="aok"
    id = db.Column(db.Integer, primary_key=True)
    popularity = db.Column(db.Enum(Level))
    # giver = db.Column(db.Integer, db.ForeignKey('actor.id'))
    # receiver = db.Column(db.Integer, db.ForeignKey('actor.id'))
    context =  db.Column(db.Integer, db.ForeignKey('context.id'))
    # prompts = db.relationship('Prompt')
    
class Gratitudeact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    popularity = db.Column(db.Enum(Level))
    message = db.Column(db.String(1000))
    giver = db.Column(db.Integer, db.ForeignKey('giver.id'))
    receiver = db.Column(db.Integer, db.ForeignKey('receiver.id'))
    context =  db.Column(db.Integer, db.ForeignKey('context.id'))
    prompts = db.relationship('Prompt')
    # act_actors = db.relationship('Actactors')
    
 
# this can be used to raise motivation for actors by telling them how gratitude (and kindness in general) can positively impact others and them    
class GratitudeImpactInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(1000))
 
             
# class Actor(db.Model):
#       id = db.Column(db.Integer, primary_key=True)
#     #   name = db.Column(db.String(1000))
#     #   email = db.Column(db.String(150), unique=True)
#       motivation = db.Column(db.Enum(Level))
#       Ability = db.Column(db.Enum(Level)) 
#     #   type = db.Column(db.Enum(ActorType))
#     #   acts = db.relationship('Gratitudeact')
#       user = db.Column(db.Integer, db.ForeignKey('user.id'))      

class Giver(db.Model):
      id = db.Column(db.Integer, primary_key=True)
    #   name = db.Column(db.String(1000))
    #   email = db.Column(db.String(150), unique=True)
      motivation = db.Column(db.Enum(Level))
      Ability = db.Column(db.Enum(Level)) 
    #   type = db.Column(db.Enum(ActorType))
    #   acts = db.relationship('Gratitudeact')
      user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
      
      def getName(self):
          user  = User.query.filter_by(id=self.user_id).first()
          if user is not None:
              return user.name 
      
      def getEmail(self):
          user  = User.query.filter_by(id=self.user_id).first()
          if user is not None:
              return user.email 
      
        
class Receiver(db.Model):
      id = db.Column(db.Integer, primary_key=True)
    #   name = db.Column(db.String(1000))
    #   email = db.Column(db.String(150), unique=True)
      motivation = db.Column(db.Enum(Level))
      Ability = db.Column(db.Enum(Level)) 
    #   type = db.Column(db.Enum(ActorType))
    #   acts = db.relationship('Gratitudeact')
      user = db.Column(db.Integer, db.ForeignKey('user.id'))  
      
         
# this class characterises the context for an act... for now it just specifies time, but later can include other parameters such as space, equipment
class Context(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    kind_acts = db.relationship('Gratitudeact')           
      
            
class Prompt(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   type = db.Column(db.Enum(PromptType)) 
   giverMessage = db.Column(db.String(1000))
   gratitude_act = db.Column(db.Integer, db.ForeignKey('gratitudeact.id'))
   
   
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    giver = db.relationship('Giver')
    receiver = db.relationship('Receiver')
    
       