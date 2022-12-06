from models import Gratitudeact, Giver, Receiver, User
from __init__ import db
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.security import generate_password_hash

server = None
sender_email = "kindness.computing@gmail.com"


def test():
    
    # fillWithDummyData()
    
    giver = Giver.query.filter_by(name="Faeq").first()
    receiver = Receiver.query.filter_by(name="Tom").first()
    
    gratAct = Gratitudeact.query.first()
    # print("grat: ", gratAct.message)
    # actors = Actor.query.all()
    
    sendEmailToGiver(giver, gratAct)
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
    # gratitude_tree_link = "https://gratitude-tree.org/"
    
    ### email content construction: plain text
 
   
    gratEmail = GratitudeEmail(recipientName=giver.name, recipientEmail=giver.email, gratitudeMessage=gratitude_msg, greetings="Good Evening", ender="Thank you for brightening one's day!")
    emailHandler = EmailHandler()
    emailHandler.sendFancyGratitudeEmail(gratEmail)  
  
    
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
    
    
def addUser(name, email, password)->User:
    
    
    ## if already exists return none
    if User.query.filter_by(email=str(email)).first():
        return None
    
    newUser = User(name=name,email=email,password=generate_password_hash("asd12345", method='sha256'))    
    
    db.session.add(newUser)
    db.session.commit()
    
    return newUser


class GratitudeEmail:
    def __init__(self, recipientEmail, subject="Be Thankful today!", recipientName="Gratituder",  greetings="Hi", gratitudeMessage="I appreciate the work you have been doing", ender="Best wishes", signature="Kind Computing", gratitudeTree="https://gratitude-tree.org/"):
        self.subject = subject
        self.recipientName = recipientName
        self.recipientEmail = recipientEmail
        self.greetings = greetings
        self.gratitudeMessage = gratitudeMessage     
        self.ender = ender
        self.signature = signature
        self.gratitudeTree = "https://gratitude-tree.org/"
        self.HTMLContent =  """<html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    </head>
    <body>
        <p>
        How about doing a small <b>gratitude</b> act? 
        You can add a leaf, saying "<i>{}</i>", on the <a href="{}">Gratitude tree</a>
        </p>
    </body>
    </html>""".format(self.gratitudeMessage, self.gratitudeTree)
    
        self.plainContent = """
        
        How about doing a Gratitude act of the day? you add a leaf, saying "{}", on the gratitude tree ({})
        """.format(self.gratitudeMessage, self.gratitudeTree)
        
    def setHTMLContent(self, HTMLContent):
        self.HTMLContent = HTMLContent
        
    def setPlainContent(self, plainContent):
        self.plainContent = plainContent
                    
    def __str__(self):
        return self.getEmailWithContent(self.plainContent)   
    
    def getHTMLEmailWithSubject(self):
        return self.getEmailWithContent(self.HTMLContent)
    
    def getHTMLEmailWithContentOnly(self):
        return self.getEmailWithContentOnly(self.HTMLContent)
    
    def getPlainEmailWithSubject(self):
        return self.getEmailWithSubjectAndContent(self.plainContent)
    
        
    def getPlainEmailWithContentOnly(self):
        return self.getEmailWithContentOnly(self.plainContent)
        
    def getEmailWithSubjectAndContent(self, content):
        return """\
    Subject: {}
    
    {} {}
    
    {}
    
    {}<br>
    --<br>
    {}
    """.format(self.subject, self.greetings, self.recipientName, content, self.ender, self.signature)
    
    
    def getEmailWithContentOnly(self, content):
        return """\
    
    {} {}
    
    {}
    
    {}<br>
    --<br>
    <i>{}</i>
    """.format(self.greetings, self.recipientName, content, self.ender, self.signature)
          
###################################
#### EMAIL HANDLER
## handles all email related tasks
class EmailHandler:
    def __init__(self, smtpServer= "smtp.gmail.com", senderEmail="kindness.computing@gmail.com"):
        self.smtpServer = smtpServer
        self.senderEmail = senderEmail
        self.server = None
        
    def __str__(instance): # instance or self, or any other name is ok as long as it is the first parameter of any function in the class
        return f"SMTP Server: {instance.smtpServer}, Sender Email: {instance.senderEmail}"
        
    def establishConnectionToServer(self):
        if self.server is not None:
            return 
        
        # global server
        password = "gjpqocclovspawrx" #an in-app passsword 
        ## establish secure connection
        port = 587  # For SSL
        # Create a secure SSL context
        context = ssl.create_default_context()

        # Try to log in to server and send email
        try:
            print("creating a Gmail SMTP server connection...")
            self.server = smtplib.SMTP(self.smtpServer,port)
            # server.ehlo() # Can be omitted
            print("securing connection...")
            self.server.starttls(context=context) # Secure the connection
            # server.ehlo() # Can be omitted
            print("logging in...")
            self.server.login(self.senderEmail, password)
            
        except Exception as e:
            # Print any error messages to stdout
            print(e)
            
    def disconnectFromSMTPServer(self):
    
        if self.server is not None:
            self.server.quit()          


    def sendPlainEmail(self, recipient_email, name, subject, message):
    
        if recipient_email is None or recipient_email == "":
            print("EmailHandLer->SendPlainEmail: An email is required")
            return
        
        ## establish secure connection
        if self.server is None:
            self.establishConnectionToServer()
            
        if self.server is None:
            print("EmailHandler->SendPlainEmail: Could not connect to mail server ({}). Qutting (I'ma head out).".format(self.smtpServer))
            return

        gratEmail = GratitudeEmail(recipientEmail=recipient_email, recipientName=name, subject=subject, gratitudeMessage=message)
        msg = gratEmail.getHTMLEmail()
        
        self.sendEmail(self.senderEmail, recipient_email, msg) 

     
    def sendFancyGratitudeEmail(self, gratitudeEmail: GratitudeEmail):
        recipient_email = gratitudeEmail.recipientEmail
        name = gratitudeEmail.recipientName
        subject = gratitudeEmail.subject
        plain_message = gratitudeEmail.getPlainEmailWithContentOnly()
        html_message = gratitudeEmail.getHTMLEmailWithContentOnly()
        
        # print("html ", html_message)
        self.sendFancyEmail(recipient_email, name, subject, plain_message, html_message)
        
          
    def sendFancyEmail(self, recipient_email, name, subject, plain_message, html_message):
        
        if recipient_email is None or recipient_email == "":
            print("EmailHandler->SendFancyEmail: An email is required")
            return
        
        ## establish secure connection
        if self.server is None:
            self.establishConnectionToServer()
            
        if self.server is None:
            print("EmailHandler->SendFancyEmail: Could not connect to mail server. Qutting (I'ma head out).")
            return

        if name is None or name == "":
            name = "Gratituder"
        
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.senderEmail
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

        self.sendEmail(self.senderEmail, recipient_email, message)

    
    def sendEmail(self, senderEmail, recipientEmail, message):
        try:
            print("sending message to: ", recipientEmail)
            # print("msg  ", message)
            self.server.sendmail(senderEmail, recipientEmail, str(message))
            print("done sending")
        except Exception as e:
            # Print any error messages to stdout
            print(e)