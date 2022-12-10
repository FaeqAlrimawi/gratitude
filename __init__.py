from venv import create
from flask import Flask
# from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager
from flask_mail import Mail



db = SQLAlchemy()
DB_NAME = "database.db"
mail = None

def create_app():
    global mail
    app = Flask(__name__)    
    app.config['SECRET_KEY'] = 'sdlgjfaiowejklvmd4%$%^DFSFD8979iJGHNDS5wgfb&^*HGHDt67dHSRTEGZHSftyretz' ## secret key
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'kindness.computing'
    app.config['MAIL_PASSWORD'] = "gjpqocclovspawrx"
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True # True if Port = 465
    mail = Mail(app)
    
    # where the data
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    # initialise DB
    db.init_app(app)

    
    # register views
    from views import views
    # from .auth import auth
    app.register_blueprint(views, url_prefix="/") # prefix for the view
    # app.register_blueprint(auth, url_prefix="/")


    from models import User
    
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    
    return app


def create_database(app):
    if not path.exists(DB_NAME):
        db.create_all(app=app)
        # db.create_scoped_session()
        print('### created database')
        

