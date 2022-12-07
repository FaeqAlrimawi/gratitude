import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



##########################################
##########################################
##### GRATITUDE EMAIL
## Special class to construct gratitude emails
class GratitudeEmail:
    def __init__(self, recipientEmail, subject="Be Thankful today!", recipientName="Gratituder",  greetings="Hi", gratitudeMessage="I appreciate the work you have been doing", gratitudeTree="https://gratitude-tree.org/", ender="Best wishes", signature="Kind Computing"):
        self.subject = subject
        self.recipientName = recipientName
        self.recipientEmail = recipientEmail
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
    
        self.plainContent = """How about doing a Gratitude act of the day? you add a leaf, saying "{}", on the gratitude tree ({})
        """.format(self.gratitudeMessage, self.gratitudeTree)
      
    def setGratitudeTreeLink(self, grattitudeTreeLink):
        self.gratitudeTree = grattitudeTreeLink
            
    def setHTMLContent(self, HTMLContent):
        self.HTMLContent = HTMLContent
        
    def setPlainContent(self, plainContent):
        self.plainContent = plainContent
                    
    def __str__(self):
        return self.getEmailWithContent(self.plainContent)   
    
    # def getHTMLEmailWithSubject(self):
    #     return self.getEmailWithContent(self.HTMLContent)
    
    def getHTMLEmailWithContentOnly(self):
        
        if self.HTMLContent is None:
            return None
        
        return self.getEmailWithContentOnly(self.HTMLContent)
    
    # def getPlainEmailWithSubject(self):
    #     return self.getEmailWithSubjectAndContent(self.plainContent)
    
        
    def getPlainEmailWithContentOnly(self):
        
        if self.plainContent is None:
            return None
        
        return self.getEmailWithContentOnly(self.plainContent)
        
    def getEmailWithSubjectAndContent(self, content):
        return """\
            
    Subject: {}
    \n\n
    {} {}
    
    {}
    
    {}
    
    
    {}
    """.format(self.subject, self.greetings, self.recipientName, content, self.ender, self.signature)
    
    
    def getEmailWithContentOnly(self, content):
        return """\
    
    {} {}
    
    {}
    
    {}
    
    {}
    """.format(self.greetings, self.recipientName, content, self.ender, self.signature)
          

##########################################
##########################################
#### EMAIL HANDLER
## handles all email related tasks, e.g. establish connection, send email
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

    def checkSMTPServerConnection(self):
         ## establish secure connection
        if self.server is None:
            self.establishConnectionToServer()
            
        if self.server is None:
            print("EmailHandler->SendFancyEmail: Could not connect to mail server. Qutting (I'ma head out).")
            return
        
        
    # def sendPlainGratitudeEmail(self, gratitudeEmail: GratitudeEmail):
       
    #     self.checkSMTPServerConnection()
       
    #     message = gratitudeEmail.getPlainEmailWithSubject()
        
    #     # print(message)
        
    #     self.sendEmail(self.senderEmail, gratitudeEmail.recipientEmail, message)
     
        
    # def sendPlainEmail(self, recipient_email, name, subject, message):
    
    #     if recipient_email is None or recipient_email == "":
    #         print("EmailHandLer->SendPlainEmail: An email is required")
    #         return
        
    #     self.checkSMTPServerConnection()

    #     gratEmail = GratitudeEmail(recipientEmail=recipient_email, recipientName=name, subject=subject, gratitudeMessage=message)
    #     msg = gratEmail.getPlainEmailWithSubject()
        
    #     self.sendEmail(self.senderEmail, recipient_email, msg) 

     
    def sendGratitudeEmail(self, gratitudeEmail: GratitudeEmail):
        recipient_email = gratitudeEmail.recipientEmail
        name = gratitudeEmail.recipientName
        subject = gratitudeEmail.subject
        plain_message = gratitudeEmail.getPlainEmailWithContentOnly()
        html_message = gratitudeEmail.getHTMLEmailWithContentOnly()
        
        # print("html ", html_message)
        self.sendEmail(recipient_email, name, subject, plain_message, html_message)
        
          
    def sendEmail(self, recipient_email, name, subject, plain_message, html_message=None):
        
        if recipient_email is None or recipient_email == "":
            print("EmailHandler->SendFancyEmail: An email is required")
            return
        
        self.checkSMTPServerConnection()

        if name is None or name == "":
            name = "Gratituder"
        
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.senderEmail
        message["To"] = recipient_email
        
        text = plain_message
        html = html_message
        
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain") if text is not None else None
        part2 =  MIMEText(html, "html") if html is not None else None
         
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1) if part1 is not None else None
        message.attach(part2) if part2 is not None else None

        self.email(self.senderEmail, recipient_email, message)

    
    def email(self, senderEmail, recipientEmail, message):
        try:
            print("sending message to: ", recipientEmail)
            # print("msg  ", message)
            self.server.sendmail(senderEmail, recipientEmail, str(message))
            print("done sending")
        except Exception as e:
            # Print any error messages to stdout
            print(e)