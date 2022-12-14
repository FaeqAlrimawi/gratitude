# import smtplib, ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
from flask_mail import Message
from flask import render_template
from __init__ import mail, app
# import threading
from datetime import datetime, timedelta
from apscheduler.events import EVENT_JOB_MISSED 
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from pytz import utc

# jobs = []
scheduler = None
# lock = threading.Lock()

##########################################
##########################################
##### GRATITUDE EMAIL
## Special class to construct gratitude emails
class GratitudeEmail(Message):
    def __init__(self, sender="kindness.computing@gmail.com", recipients = None, subject="Be Thankful today!", recipientName="Gratituder",  greetings="Hi", gratitudeMessage="I appreciate the work you have been doing", gratitudeTree="https://gratitude-tree.org/", ender="Best wishes", signature="Kind Computing"):
        super(GratitudeEmail, self).__init__(subject=subject, recipients=recipients, sender=sender)
        self.recipients = recipients if type(recipients) is list else [recipients]
        self.recipientName = recipientName
        self.greetings = greetings
        self.gratitudeMessage = gratitudeMessage     
        self.ender = ender
        self.signature = signature
        self.gratitudeTree = gratitudeTree
        self.html = self.setContent("email_reminder.html")
        self.body = self.setContent("email_page.txt")
        
    def setContent(self, email_page):
        return render_template(email_page, greetings=self.greetings, recipient_name=self.recipientName, gratitudeMessage=self.gratitudeMessage, gratitudeTreeLink=self.gratitudeTree, ender=self.ender, signature=self.signature)

        
##########################################
##########################################
#### EMAIL HANDLER
## handles all email related tasks, e.g. establish connection, send email
class EmailHandler:

    # scheduler = None
    
    def __init__(self):
        self.init_scheduler()
        self.scheduled_jobs = []
        scheduler.add_listener(self.schedule_listener, EVENT_JOB_MISSED)
             
    def init_scheduler(self):
        global scheduler
    
        if scheduler is not None:
            return 
        
        print("##### EmailHandler: initializing scheduler ######")
    

        jobstores = {
        # 'mongo': MongoDBJobStore(),
        'default': SQLAlchemyJobStore(url=app.config['SQLALCHEMY_DATABASE_URI'])
        }
        executors = {
            'default': ThreadPoolExecutor(10), # more can cause "connection unexpectedly closed" 
            'processpool': ProcessPoolExecutor(1) # more can cause "connection unexpectedly closed" 
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 3,
            'misfire_grace_time': None
        }

        scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
        # sched.add_jobstore('sqlalchemy', url=app.config['SQLALCHEMY_DATABASE_URI'])
        
        scheduler.start()
    
        if scheduler is not None:
            pendingJobs = scheduler.get_jobs()
            if len(pendingJobs) > 0:
                print("scheduled jobs: ", scheduler.get_jobs())
                # print("############ CLEARING SCHEDULE")
                # scheduler.remove_all_jobs()
                # for pendingJob in pendingJobs:
                #     print("resume job-name: ", pendingJob.name)
                    # new_run_time = datetime.now() + timedelta(seconds=random.randint(1, 60))
                    # pendingJob.reschedule(trigger="date", run_date=new_run_time)
                    # scheduler.reschedule_job
                    # pendingJob.resume()  
        # atexit.register(lambda: scheduler.shutdown())
    
    # return scheduler

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
         
    def sendGratitudeEmail(self, gratitudeEmail: GratitudeEmail):
        # gratitudeEmail.prepareMessage()
        self.email(gratitudeEmail)
        
            
    # @sched.scheduled_job('cron', day_of_week='mon-fri', hour=18)
    def schedule_emails_weekly(self, gratitudeEmail, start_date=None, end_date=None, send_time=None):  
        """Schedules emails to be sent between the given start and end dates (end date excluded) at the given send_time.
        Emails are only sent during week-days (mon-fri).

        Args:
            gratitudeEmail (GratitudeEmail): A GratitudeEmail object holding information about the email to be sent (e.g., recipients)
            
            start_date (datetime | str [format: "yyyy-mm-dd"], optional): the starting date to send emails. Defaults to None
            
            end_date (datetime | str [format: "yyyy-mm-dd"], optional): the end date to stop sending emails. Defaults to None.
            
            send_time (datetime | str [format: "hh:mm:ss"], optional): the time of the day to send emails (uses 24h system). Defaults to None.
            
        If end_date is None then the scheduler will go indefinite sending emails
        If send_time is None then the scheduler will send emails at a time equal to the time the job was created.    
        """
        global scheduler
        
        ## set time
        if send_time is not None:
            hour, min, sec = send_time.hour, send_time.minute, send_time.second
        else:
            now = datetime.now() + timedelta(seconds=10)
            hour, min, sec = now.hour, now.minute, now.second

        ## trigger can be: 
        # date: run the job just once at a certain point of time,
        # interval: run the job at fixed intervals of time, or 
        # cron: run the job periodically at certain time(s) of day.
        # One can implement their own trigger. 
        ## misfire_grace_time is None meaning it will try to send the email (do the job) as soon as it can
        
        job = scheduler.add_job(self.sendGratitudeEmail, trigger='cron', start_date=start_date, end_date=end_date, 
                                    day_of_week="mon-fri", hour=hour, minute=min, second=sec, jitter=120,  args=[gratitudeEmail],  name="{}:{}".format(gratitudeEmail.recipients, send_time))
        
        self.scheduled_jobs.append(job)
        
    

    def schedule_email_at(self, gratitudeEmail, send_time):  
        """Sends a gratitude email at the given send_time 

        Args:
            gratitudeEmail (GratitudeEmail): GratitudeEmail object holding info about the email to be sent (e.g., recipients)
            
            send_time (datetime): Time to send the email
        """
        
        ## trigger can be: 
        # date: run the job just once at a certain point of time,
        # interval: run the job at fixed intervals of time, or 
        # cron: run the job periodically at certain time(s) of day.
        # One can implement their own trigger. 
        ## misfire_grace_time is None meaning it will try to send the email (do the job) as soon as it can
        
        global scheduler
        
        job = scheduler.add_job(self.sendGratitudeEmail, trigger='date', run_date=send_time,  args=[gratitudeEmail])
        
        self.scheduled_jobs.append(job)
        
    
            
    def schedule_listener(event):
    ##TODO: listen to event_job_missed
        print(event)  
        
        
    def shutdown_scheduler(self):
        scheduler.shutdown(wait=True)             