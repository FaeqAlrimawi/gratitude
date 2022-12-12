import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_mail import Message
from __init__ import mail, app
import threading
from datetime import datetime


lock = threading.Lock()

##########################################
##########################################
##### GRATITUDE EMAIL
## Special class to construct gratitude emails
class GratitudeEmail(Message):
    def __init__(self, sender="kindness.computing@gmail.com", recipients = None, subject="Be Thankful today!", recipientName="Gratituder",  greetings="Hi", gratitudeMessage="I appreciate the work you have been doing", gratitudeTree="https://gratitude-tree.org/", ender="Best wishes", signature="<br><br>--<br>Kind Computing"):
        super(GratitudeEmail, self).__init__(subject=subject, recipients=recipients, sender=sender)
        self.recipients = recipients if type(recipients) is list else [recipients]
        self.recipientName = recipientName
        self.greetings = greetings
        self.gratitudeMessage = gratitudeMessage     
        self.ender = ender
        self.signature = signature
        self.gratitudeTree = gratitudeTree
        
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
    
        # self.html = self.getEmailWithContentOnly(self.HTMLContent)
        
        self.plainContent = """How about doing a Gratitude act of the day? you add a leaf, saying "{}", on the gratitude tree ({})
        """.format(self.gratitudeMessage, self.gratitudeTree)
    
        # self.body = self.getEmailWithContentOnly(self.plainContent)

    def setHTMLContent(self, htmlContent):
        self.HTMLContent = htmlContent
        # self.html = self.getEmailWithContentOnly(htmlContent)
        
    def setPlainContent(self, plainContent):
        self.plainContent = plainContent
        # self.body = self.getEmailWithContentOnly(plainContent)    
        
    def getEmailWithContentOnly(self, content):
        return """\
    
    {} {}
    
    {}
    
    {}
    
    
    {}
    """.format(self.greetings, self.recipientName, content, self.ender, self.signature)
          
    def prepareMessage(self):
        self.html = self.getEmailWithContentOnly(self.HTMLContent)
        self.body = self.getEmailWithContentOnly(self.plainContent)
        
##########################################
##########################################
#### EMAIL HANDLER
## handles all email related tasks, e.g. establish connection, send email
class EmailHandler:

     
    def sendGratitudeEmail(self, gratitudeEmail: GratitudeEmail):
        gratitudeEmail.prepareMessage()
        self.email(gratitudeEmail)
        
    
    def email(self, message):
        try:
            with app.app_context():
                # print("sending message to: ", recipientEmail)
                # print(message)
                # print("EmailHandler->email: sending email to: ", message.recipients)
                # mail.connect()
                mail.send(message)
                print("EmailHandler->email: sent to {} at {}".format(message.recipients, datetime.now()))
        except Exception as e:
            # Print any error messages to stdout
            print(e)