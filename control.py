from models import Gratitudeact, Giver, Receiver
from __init__ import db
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

server = None
sender_email = "kindness.computing@gmail.com"


def test():
    
    # fillWithDummyData()
    
    giver = Giver.query.filter_by(name="Faeq").first()
    receiver = Receiver.query.filter_by(name="Tom").first()
    
    gratAct = Gratitudeact.query.first()
    # print("grat: ", gratAct.message)
    # actors = Actor.query.all()
    
    sendEmailToGiver(receiver, gratAct)
    # print(giver.name,giver.email)
    
    
def sendEmailToGiver(giver, gratitudeAct):
    
    if giver is None or not isinstance(giver, Giver):
        print("no giver")
        return
    
    if giver.email is None or giver.email == "":
        print("no email found")
        return
    
    if gratitudeAct is not None and isinstance(gratitudeAct, Gratitudeact):
        gratitude_msg = gratitudeAct.message
    else:
        gratitude_msg = "Thank you" # default gratitude message
            
    ### link to gratitude tree to where the giver should be adding a leaf
    gratitude_tree_link = "https://gratitude-tree.org/"
    
    ### email content construction: plain text
    plain_msg = """\
        How about doing a small Gratitude act? you can add a leaf, saying {}, on the Gratitude tree ({}).  
        """.format(gratitude_msg, gratitude_tree_link)
        
    ### email content construction: plain text    
    html_msg = """\
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
  <body>
   
    <p>
    
       How about doing a small <b>gratitude</b> act? you can add a leaf, saying <i>{}</i>, on the <a href="{}">Gratitude tree</a>
    </p>
  </body>
</html>
""".format(gratitude_msg, gratitude_tree_link)
    
    sendFancyEmail(giver.email, giver.name,"Time to be thankful", plain_msg, html_msg)  
  
  
def sendPlainEmail(recipient_email, name, subject, message):
    global sender_email
    
    if recipient_email is None or recipient_email == "":
        print("control->SendEmail: An email is required")
        return
    
    ## establish secure connection
    if server is None:
        establishConnectionToGmailServer()
        
    if server is None:
        print("Could not connect to mail server. Qutting (I'ma head out).")
        return

    if name is None or name == "":
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
    
    
    
def sendFancyEmail(recipient_email, name, subject, plain_message, html_message):
    global sender_email
    
    if recipient_email is None or recipient_email == "":
        print("control->SendEmail: An email is required")
        return
    
    ## establish secure connection
    if server is None:
        establishConnectionToGmailServer()
        
    if server is None:
        print("Could not connect to mail server. Qutting (I'ma head out).")
        return

    if name is None or name == "":
        name = "Gratituder"
    
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email
    
    text = plain_message
    html = html_message
    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    try:
        print("sending message to: ", recipient_email)
        server.sendmail(sender_email, recipient_email, message.as_string())
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
    smtp_server = "smtp.gmail.com"
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
    
    
def fillWithDummyData():
    
    ##gratitude act
    gratAct = Gratitudeact(message="I appreciate your work on the event :)")
    db.session.add(gratAct)
    db.session.commit()
    
    ## giver and receiver
    giver = Giver(name="Faeq", email="faeq.rimawi@gmail.com")
    receiver = Receiver(name="Tom")
    
    db.session.add(giver)
    db.session.add(receiver)
    db.session.commit()
    # return    