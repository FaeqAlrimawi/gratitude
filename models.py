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
    
         
class Actofkindness(db.Model):
    __name__="aok"
    id = db.Column(db.Integer, primary_key=True)
    popularity = db.Column(db.Enum(Level))
    giver = db.Column(db.Integer, db.ForeignKey('actor.id'))
    receiver = db.Column(db.Integer, db.ForeignKey('actor.id'))
    context =  db.Column(db.Integer, db.ForeignKey('context.id'))
    
class Gratitudeact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    popularity = db.Column(db.Enum(Level))
    gratitudeMessage = db.Column(db.String(1000))
    actor = db.Column(db.Integer, db.ForeignKey('actor.id'))
    context =  db.Column(db.Integer, db.ForeignKey('context.id'))
    prompts = db.relationship('Prompt')
   
    
    
# this can be used to raise motivation for actors by telling them how gratitude (and kindness in general) can positively impact others and them    
class GratitudeImpactInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(1000))
 
             
class Actor(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(1000))
      email = db.Column(db.String(150), unique=True)
      motivation = db.Column(db.Enum(Level))
      Ability = db.Column(db.Enum(Level)) 
      type = db.Column(db.Enum(ActorType))
      acts = db.relationship('Gratitudeact')
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
    first_name = db.Column(db.String(150))
    actor = db.relationship('Actor')
    
       