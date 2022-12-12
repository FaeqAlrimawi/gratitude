from models import Gratitudeact, Giver, Receiver, User
from __init__ import db, scheduler
from werkzeug.security import generate_password_hash
from EmailHandler import GratitudeEmail, EmailHandler
import random
from apscheduler.events import EVENT_JOB_MISSED 
# from __init__ import scheduler
from flask import render_template 
from datetime import datetime, timedelta



emailHandler = EmailHandler()
jobs = []
# server = None
# sender_email = "kindness.computing@gmail.com"
# givers_global = None
# gratitudeAct_global = None

def test():
    
    # fillWithDummyData()

    givers = Giver.query.all()
    num = 20
    # receiver = Receiver.query.filter_by(name="Tom").first()
    print("send to: ", len(givers[:num]))
    
    # getRandomGratitudeAct()
    # gratAct = Gratitudeact.query.all()
    # print(gratAct)
    # print("grat: ", gratAct.message)
    # actors = Actor.query.all()
    # send_time = datetime(2022,12,12,14,20,00)
    sendGratitudeEmailToGivers(givers[:num])
    
    # print(giver.name,giver.email)
                   
                   
def sendGratitudeEmailToGivers(givers, gratitudeAct="random", send_time=None):
        
    if givers is None:
        print("No givers. Please provide at least one giver")
        return
    
    # emailHandler = EmailHandler()
    
     
    if type(givers) is not list: givers = [givers]
    
    for giver in givers:
        
        if type(giver) is not Giver: continue
        
        giverEmail = giver.getEmail()
        giverName = giver.getName()
        
        if giverEmail is None or giverEmail == "":
            print("no email found for Giver: {}".format(giverName))
            continue
        
        if type(gratitudeAct) is Gratitudeact:
            gratitude_msg = gratitudeAct.message
        elif type(gratitudeAct) is str and gratitudeAct == "random":
            randGratitudeAct = getRandomGratitudeAct()
            
            gratitude_msg = randGratitudeAct.message if randGratitudeAct is not None else "Thank you!" 
        else:    
            gratitude_msg = "Thank you!" # default gratitude message
                
        ### email content construction: plain text
        gratEmail = GratitudeEmail(recipientName=giverName, recipients=giverEmail, gratitudeMessage=gratitude_msg, greetings="Good Evening", ender="Thank you for brightening one's day!")
        # gratEmail.setHTMLContent(None)
        gratEmail.setHTMLContent(render_template("email_page.html", gratitudeMessage=gratEmail.gratitudeMessage, gratitudeTreeLink=gratEmail.gratitudeTree))
        ## schedule send
        
        if send_time is None: # send in a random time between 1 and the number 120 (avoid sending all at the same time)
            new_send_time = datetime.now() + timedelta(seconds=random.randint(1, 60))
            
            # print(new_send_time)
        
        scheduled_email(gratEmail,new_send_time) 
    
    # print_jobs()
  
    # exit()
# def print_jobs():
#     print(jobs)
     
 # @sched.scheduled_job('cron', day_of_week='mon-fri', hour=18)
def scheduled_email(gratitudeEmail, send_time):  
    
    # print("whaaat")
    emailHandler = EmailHandler()
    # in case it misses the job give it a next time with a random period of max. 120 seconds
    # next_run_time = send_time + timedelta(seconds=random.randint(1, 120))
    
    hour, min, sec, microsec = send_time.hour, send_time.minute, send_time.second, send_time.microsecond
    
    # print(hour, min, sec, microsec)
    
    ## trigger can be: 
    # date: run the job just once at a certain point of time,
    # interval: run the job at fixed intervals of time, or 
    # cron: run the job periodically at certain time(s) of day.
    # One can implement their own trigger. 
    ## misfire_grace_time is None meaning it will try to send the email (do the job) as soon as it can
    jobs.append(scheduler.add_job(emailHandler.sendGratitudeEmail, trigger='cron', day_of_week='mon',hour=hour, minute=min, second=sec,   args=[gratitudeEmail],  name="{}:{}".format(gratitudeEmail.recipients, send_time)))
    scheduler.add_listener(schedule_listener, EVENT_JOB_MISSED)
    # print("Email scheduled to send: \nAt: {} (next run: {}), \nTo: {}".format(send_time, next_run_time, gratitudeEmail.recipients))
    
    # emailHandler.sendGratitudeEmail(msg)
# sched.start()

def schedule_listener(event):
    ##TODO: listen to event_job_missed
    print(event)
       
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
    
    # if Giver.query.filter_by(user_id=gmailUser.id).first() is None:
    # for testing
    for i in range(70):
        gmailGiver = Giver(user_id=gmailUser.id) 
        db.session.add(gmailGiver)
    
    # if Giver.query.filter_by(user_id=leroUser.id).first() is None:        
    #     leroGiver = Giver(user_id=leroUser.id)
    #     db.session.add(leroGiver)
        
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
    ##TODO: look for a better way
    
    # for grat in Gratitudeact.query.all():
    #     print(grat.id)
        
    return Gratitudeact.query.get(random.randint(1, Gratitudeact.query.count()))

