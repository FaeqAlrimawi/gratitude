from . import db
import enum

class Level(enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    
    
class Act(db.Model):
    __name__="act"
    id = db.Column(db.Integer, primary_key=True)
    
    
class Actofkindness(db.Model, Act):
    __name__="aok"
    id = db.Column(db.Integer, primary_key=True)
    popularity = db.Column(db.Enum(Level))
    giver = db.Column(db.Integer, db.ForeignKey('actor.id'))
    receiver = db.Column(db.Integer, db.ForeignKey('actor.id'))
    
class GratitudeAct(db.Model, Actofkindness):
    gratitudeMessage = db.Column(db.String(1000))
    
    
# this can be used to raise motivation for actors by telling them how gratitude (and kindness in general) can positively impact others and them    
class GratitudeImpactInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(1000))
 
             
class Actor(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(1000))
      email = db.Column(db.String(150), unique=True)
      motivation = db.Column(Level)
      Ability = db.Column(Level) 
      acts_performed = db.relationship('Actofkindness')
      acts_received = db.relationship('Actofkindness')       