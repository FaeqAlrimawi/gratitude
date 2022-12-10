from models import Gratitudeact, Giver, Receiver, User
from __init__ import db
from werkzeug.security import generate_password_hash
from EmailManager import GratitudeEmail, EmailHandler
import random
import schedule
import datetime as dt
import time
from utils.time import get_seconds
import threading 
# from uwsgidecorators import thread 
from flask_restful import Resource

# server = None
# sender_email = "kindness.computing@gmail.com"
givers_global = None
gratitudeAct_global = None

def test():
    
    # fillWithDummyData()
    
    givers = Giver.query.all()
    # receiver = Receiver.query.filter_by(name="Tom").first()
    print(givers)
    
    gratAct = Gratitudeact.query.all()
    print(gratAct)
    # print("grat: ", gratAct.message)
    # actors = Actor.query.all()
    
    sendGratitudeEmailToGivers_at(givers, repeat="once", send_time="15:46:00")
    # print(giver.name,giver.email)
    

def sendGratitudeEmailToGivers_at(givers, gratitudeAct="random", repeat="once", send_time="now"): 
     
    match repeat:
            case "once":
                if send_time == "now":
                    sendGratitudeEmailToGivers(givers, gratitudeAct)
                else:        
                    #TODO: FIX this
                    hh, mm, ss = send_time.split(':')
                    send_time_obj = dt.datetime(year=dt.date.today().year, month=dt.date.today().month, day=dt.date.today().day, hour=int(hh), minute=int(mm), second=int(ss))
                    now_time = dt.datetime.today()
                    time_diff = (send_time_obj - now_time).total_seconds()
                    print(time_diff)
                    # time.sleep(time_dff)
                    global givers_global
                    global gratitudeAct_global
                    
                    givers_global = givers
                    gratitudeAct_global = gratitudeAct
                    # thread = threading.Thread(target=sendGratitudeEmailToGivers, args=(givers_global, gratitudeAct_global))
                    # thread.daemon = True
                    # thread.start()
                    sendGratitudeEmailToGivers(givers, gratitudeAct)
            case "daily":
                schedule.every(30).seconds.do(sendGratitudeEmailToGivers(givers, gratitudeAct))  
    
                while True:
                    schedule.run_pending()
                    time.sleep(1)
    # time.sleep(10)                   
                   
def sendGratitudeEmailToGivers(givers, gratitudeAct="random", waiting_time=0):
    
    ### repeat parameter takes:
    # once: happens once at the given time
    # daily: at the given time every day
    # weekly: every week the given time
  
    if waiting_time >0:
        time.sleep(waiting_time)
        
    if givers is None:
        print("No givers. Please provide at least one giver")
        return
    
    emailHandler = EmailHandler()
    
     
    if type(givers) is not list: givers = [givers]
    
    for giver in givers:
        
        if type(giver) is not Giver: continue
        
        giverEmail = giver.getEmail()
        giverName = giver.getName()
        
        if giverEmail is None or giverEmail == "":
            print("no email found for Giver: {}".format(giverName))
            return
        
        if type(gratitudeAct) is Gratitudeact:
            gratitude_msg = gratitudeAct.message
        elif type(gratitudeAct) is str and gratitudeAct == "random":
            #TODO: Select random act
            randGratitudeAct = getRandomGratitudeAct()
            
            gratitude_msg = randGratitudeAct.message if randGratitudeAct is not None else "Thank you!" 
        else:    
            gratitude_msg = "Thank you!" # default gratitude message
                
        ### email content construction: plain text
        gratEmail = GratitudeEmail(recipientName=giverName, recipientEmail=giverEmail, gratitudeMessage=gratitude_msg, greetings="Good Evening", ender="Thank you for brightening one's day!")
        # gratEmail.setHTMLContent(None)
        
        ## schedule send
        
        emailHandler.sendGratitudeEmail(gratEmail) 
  
    
def fillWithDummyData():
    
    ##gratitude act
    msgs = ["I appreciate your work on the event :)", "Thank you very much for all the hard work", "What an amazing person you are!"]
    
    for msg in msgs:
        if Gratitudeact.query.filter_by(message=msg).first() is None:
            gratAct = Gratitudeact(message=msg)
            db.session.add(gratAct)
            db.session.commit()
    
    ## first user
    gmailUser = addUser(name="Faeq", email="faeq.rimawi@gmail.com", password="asd123")
    gmailUser = getUser("faeq.rimawi@gmail.com") if gmailUser is None else None
    
    ### another user
    leroUser = addUser(name="Lero", email="faeq.alrimawi@lero.ie", password="asd123")
    leroUser = getUser("faeq.alrimawi@lero.ie") if leroUser is None else None
    
    if Giver.query.filter_by(user_id=gmailUser.id).first() is None:
        gmailGiver = Giver(user_id=gmailUser.id) 
        db.session.add(gmailGiver)
    
    if Giver.query.filter_by(user_id=leroUser.id).first() is None:        
        leroGiver = Giver(user_id=leroUser.id)
        db.session.add(leroGiver)
        
    db.session.commit()
    
    
def addUser(name, email, password)->User:
    
    
    ## if already exists return none
    if getUser(email) is not None:
        return None
    
    newUser = User(name=name,email=email,password=generate_password_hash(password, method='sha256'))    
    
    db.session.add(newUser)
    db.session.commit()
    
    return newUser


def getUser(email) -> User:
    
    if type(email) is not str:
        return None 
    
    return User.query.filter_by(email=str(email)).first()


def getRandomGratitudeAct() -> Gratitudeact:
    
    print(Gratitudeact.query.count())
    return random.choice(Gratitudeact.query.all())

