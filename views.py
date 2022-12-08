from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_user
from models import User
from werkzeug.security import generate_password_hash
from __init__ import db
from control import test,addUser


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
    
    test()
    return render_template("home.html", user=current_user)


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