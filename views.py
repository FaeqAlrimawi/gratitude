from flask import Blueprint, render_template
from flask_login import current_user, login_user
from models import User
from werkzeug.security import generate_password_hash
from __init__ import db

views = Blueprint("views", __name__)

# the route of our website
@views.route('/', methods=['GET', 'POST'])
def home():
    
    myEmail="faeq.rimawi@gmail.com"
         
    if User.query.filter_by(email=myEmail).first() is None: 
        new_user = User(email=myEmail, first_name="faeq", password=generate_password_hash("asd12345", method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
    
    return render_template("home.html", user=current_user)