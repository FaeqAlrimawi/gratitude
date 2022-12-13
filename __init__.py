from venv import create
from flask import Flask
# from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager
from flask_mail import Mail
# from celery import Celery
# from pytz import utc
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
# from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import atexit
# from  datetime import datetime, timedelta
# import random 


db = SQLAlchemy()
DB_NAME = "database.db"
mail = None 
app = Flask(__name__) 
# scheduler = None
# celery = Celery(app.name, broker='redis://localhost:6379/0')
 
def create_app():
    # print("################### CREATING APP")
    global mail
    global app  
    
    app.config['SECRET_KEY'] = 'sdlgjfaiowejklvmd4%$%^DFSFD8979iJGHNDS5wgfb&^*HGHDt67dHSRTEGZHSftyretz' ## secret key
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'kindness.computing' #'frimawi22' 
    app.config['MAIL_PASSWORD'] = "gjpqocclovspawrx" #"btyjwvwbjayokoug" 
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True # True if Port = 465
    mail = Mail(app)
    
    # where the data
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    # init scheduler
    # init_scheduler()
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
  
        
# def init_scheduler():
#     global scheduler
    
#     if scheduler is not None:
#         return 
    
#     print("##### initializing scheduler ######")
   

#     jobstores = {
#     # 'mongo': MongoDBJobStore(),
#     'default': SQLAlchemyJobStore(url=app.config['SQLALCHEMY_DATABASE_URI'])
#     }
#     executors = {
#         'default': ThreadPoolExecutor(15), # more can cause "connection unexpectedly closed" 
#         'processpool': ProcessPoolExecutor(2) # more can cause "connection unexpectedly closed" 
#     }
#     job_defaults = {
#         'coalesce': False,
#         'max_instances': 3,
#         'misfire_grace_time': None
#     }

#     scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
#     # sched.add_jobstore('sqlalchemy', url=app.config['SQLALCHEMY_DATABASE_URI'])
    
#     scheduler.start()
    
#     if scheduler is not None:
#         pendingJobs = scheduler.get_jobs()
#         if len(pendingJobs) > 0:
#             print("scheduled jobs: ", scheduler.get_jobs())
#             # print("############ CLEARING SCHEDULE")
#             # scheduler.remove_all_jobs()
#             # for pendingJob in pendingJobs:
#             #     print("resume job-name: ", pendingJob.name)
#                 # new_run_time = datetime.now() + timedelta(seconds=random.randint(1, 60))
#                 # pendingJob.reschedule(trigger="date", run_date=new_run_time)
#                 # scheduler.reschedule_job
#                 # pendingJob.resume()  
#     # atexit.register(lambda: scheduler.shutdown())
      
    
      
#     return scheduler


# @atexit.register
# def exit():
#     print("existing and shutting down the scheduuler.")
#     scheduler.shutdown() if scheduler is not None else None
