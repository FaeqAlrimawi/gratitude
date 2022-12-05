from models import Gratitudeact, Giver, Receiver
from __init__ import db
import smtplib, ssl
import getpass

server = None
sender_email = "kindness.computing@gmail.com"


def test():
    # gratAct = Gratitudeact(gratitudeMsg="thank you!!")
    # db.session.add(gratAct)
    # db.session.commit()
    
    giver = Giver.query.filter_by(name="Faeq").first()
    receiver = Receiver.query.filter_by(name="Tom").first()
    # giver = Giver(name="Faeq", email="faeq.rimawi@gmail.com")
    # receiver = Receiver(name="Tom")
    
    # db.session.add(giver)
    # db.session.add(receiver)
    # db.session.commit()
    
    # gratActs = Gratitudeact.query.all()
    # actors = Actor.query.all()
    
    sendEmailForGiver(giver)
    # print(giver.name,giver.email)
    
    
def sendEmailForGiver(giver):
    
    if giver is None or not isinstance(giver, Giver):
        print("not a giver")
        return
    
    if giver.email is None or giver.email is "":
        print("no email found")
        return
    
    sendEmail(giver.email, "","Time to be thankful", "how about doing a small gratitude act for the day??")  
  
  
def sendEmail(recipient_email, name, subject, message):
    global sender_email
    
    if recipient_email is None or recipient_email is "":
        print("control->SendEmail: An email is required")
        return
    
    ## establish secure connection
    if server is None:
        establishConnectionToGmailServer()
        
    if server is None:
        print("Could not connect to mail server. Qutting (I'ma head out).")
        return

    if name is None or name is "":
        name = "Gratituder"
    
    msg = """\
Subject: {}

Hi {}... 

{}""".format(subject,name,message)

    try:
        print("sending message to: ", recipient_email)
        server.sendmail(sender_email, recipient_email, msg)
        print("done sending")
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    # finally:
    #     print("qutting the smtp server")
    #     server.quit() 
    
      
def establishConnectionToGmailServer():
    global server
    global sender_email
    password = "gjpqocclovspawrx" #an in-app passsword 
    ## establish secure connection
    port = 587  # For SSL
    # Create a secure SSL context
    # context = ssl.create_default_context()
    smtp_server = "smtp.gmail.com"
    # print("pass: ", password)
    # with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    #     server.login("kindness.computing@gmail.com", password)
    
    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        print("creating a Gmail SMTP server connection...")
        server = smtplib.SMTP(smtp_server,port)
        # server.ehlo() # Can be omitted
        print("securing connection...")
        server.starttls(context=context) # Secure the connection
        # server.ehlo() # Can be omitted
        print("logging in...")
        server.login(sender_email, password)
        
    except Exception as e:
        # Print any error messages to stdout
        print(e)
       
          
def disconnectFromSMTPServer():
    
    if server is not None:
        server.quit()    
    