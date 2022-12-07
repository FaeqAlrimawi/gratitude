from models import Gratitudeact, Giver, Receiver, User
from __init__ import db
from werkzeug.security import generate_password_hash
from EmailManager import GratitudeEmail, EmailHandler

server = None
sender_email = "kindness.computing@gmail.com"


def test():
    
    fillWithDummyData()
    
    giver = Giver.query.first()
    # receiver = Receiver.query.filter_by(name="Tom").first()
    
    gratAct = Gratitudeact.query.first()
    # print("grat: ", gratAct.message)
    # actors = Actor.query.all()
    
    sendEmailToGiver(giver, gratAct)
    # print(giver.name,giver.email)
    
    
def sendEmailToGiver(giver, gratitudeAct):
    
    if giver is None or not isinstance(giver, Giver):
        print("no giver")
        return
    
    giverEmail = giver.getEmail()
    giverName = giver.getName()
    
    if giverEmail is None or giverEmail == "":
        print("no email found")
        return
    
    if gratitudeAct is not None and isinstance(gratitudeAct, Gratitudeact):
        gratitude_msg = gratitudeAct.message
    else:
        gratitude_msg = "Thank you" # default gratitude message
            
    ### link to gratitude tree to where the giver should be adding a leaf
    # gratitude_tree_link = "https://gratitude-tree.org/"
    
    ### email content construction: plain text
 
   
    gratEmail = GratitudeEmail(recipientName=giverName, recipientEmail=giverEmail, gratitudeMessage=gratitude_msg, greetings="Good Evening", ender="Thank you for brightening one's day!")
    # gratEmail.setHTMLContent(None)
    emailHandler = EmailHandler()
    emailHandler.sendGratitudeEmail(gratEmail)  
  
    
def fillWithDummyData():
    
    ##gratitude act
    gratAct = Gratitudeact(message="I appreciate your work on the event :)")
    db.session.add(gratAct)
    db.session.commit()
    
    ## giver and receiver
    user = User.query.first()
    giver = Giver(user_id=user.id)
    # receiver = Receiver(name="Tom")
    
    db.session.add(giver)
    # db.session.add(receiver)
    db.session.commit()
    # return    
    
    
def addUser(name, email, password)->User:
    
    
    ## if already exists return none
    if User.query.filter_by(email=str(email)).first():
        return None
    
    newUser = User(name=name,email=email,password=generate_password_hash("asd12345", method='sha256'))    
    
    db.session.add(newUser)
    db.session.commit()
    
    return newUser
