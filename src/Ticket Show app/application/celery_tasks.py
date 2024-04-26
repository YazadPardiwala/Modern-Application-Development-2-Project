from main import celery
from time import sleep
from random import random
from json import dumps
from httplib2 import Http
from celery.schedules import crontab

#models & stuff imports
from main import app
from application.models import *
from sqlalchemy.sql import text
from application.database import db

#smtp & mail imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

@celery.task()
def test_basic():
    sleep(4)
    return random()

@celery.task()
def g_chat_webhook():
    """Google Chat incoming webhook quickstart."""
    url = "a google chat url to receive webhooks"
    app_message = {
        'text': 'The real app says hello'}
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(app_message),
    )
    print(response)

@celery.task()
def daily_email_reminder(users):

    # launching the smtp server & logging in
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('an email id for smtp to log into', 'Once upon a time this was a code to let smtp log in to my email, it is no longer')

    # creating & sending mails
    #print(users)
    for user in users:
        # creating mail
        #print(user)
        msg = MIMEMultipart()
        msg['subject'] = f"Reminder- {user['U_NAME']}, Ticket show app"
        msg.attach(MIMEText(f"Hello {user['U_NAME']}, we noticed you did not visit our app today. Please be so kind as to do so; it is support from good ordinary folk like you that keeps our app going."))

        # sending mail

        smtp.sendmail(from_addr="t9557749@gmail.com",
                      to_addrs=user['EMAIL'], msg=msg.as_string())

        '''

    #querying the database
    users = USER.query.filter(USER.VISITED==0, USER.ADMIN==0).all()

    # creating & sending mails
    for user in users:
        # creating mail
        # print(user)
        msg = MIMEMultipart()
        msg['subject'] = f"Reminder- {user.U_NAME}, Ticket show app"
        msg.attach(MIMEText(
            f"Hello {user.U_NAME}, we noticed you did not visit our app today. Please be so kind as to do so; it is support from good ordinary folk like you that keeps our app going."))

        # sending mail

        smtp.sendmail(from_addr="t9557749@gmail.com",
                      to_addrs=user.EMAIL, msg=msg.as_string())'''

    smtp.quit()
    print('if you are reading this...cross your fingers you should have received a couple of mails')
    return 'what just happened?'




