from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_user
from models import User
from werkzeug.security import generate_password_hash
from __init__ import db, mail
from control import test,addUser
import threading
from flask_mail import Message, Mail
from EmailHandler import GratitudeEmail, EmailHandler

views = Blueprint("views", __name__)

# the route of our website
@views.route('/', methods=['GET', 'POST'])
def home():
    
    myEmail="faeq.rimawi@gmail.com"
         
    if User.query.filter_by(email=str(myEmail)).first() is None: 
        new_user = User(email=myEmail, name="Faeq", password=generate_password_hash("asd12345", method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
    
    # threading.Timer(interval=5, function=test).start()
    sendMessage()
    return render_template("home.html", user=current_user)

def sendMessage():
    msg = GratitudeEmail( recipients = ['faeq.rimawi@gmail.com'], recipientName="Faeq", greetings="good evening", gratitudeTree="https://gratitude-tree.org/tree_viewer/global-payroll-greater-goods-gratitude-tree")
        # msg.body = "Hello Flask message sent from Flask-Mail"
        # You can also use msg.html to send html templates!
    # Example:
    # msg.html = render_template("hello.html") # Template should be in 'templates' folder
    
    msg.setHTMLContent(render_template("email_page.html", gratitudeMessage=msg.gratitudeMessage, gratitudeTreeLink=msg.gratitudeTree))
   
    emailHandler = EmailHandler()
    emailHandler.sendGratitudeEmail(msg)
    return "Your email has been sent!"
       
@views.route("/get-involved", methods=["GET", "POST"])
def signUp():    
    
    if request.method == 'POST':
         form = request.form
         
         email = form.get('email')
         name = form.get('name')
         password = form.get('password1')
         
         newUser = addUser(name, email, password)
         
         if newUser is None:
             flash("Failed to register. Please try again", category="error")
         else:
             flash("{}, your registration was successful".format(name), category="success")    
    
        
    return render_template("get_involved.html", user=current_user)