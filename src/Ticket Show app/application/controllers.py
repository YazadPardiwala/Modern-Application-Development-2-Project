from main import app
from flask import Flask, request, jsonify
from application.models import *
from celery.schedules import crontab
from application.celery_tasks import *
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from sqlalchemy.sql import text
import jwt
import datetime
from main import celery
from application.validation import *
import schedule
import time

#smtp & mail imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

app.secret_key = 'its_a_secret'

def token_required(f):
    @wraps(f)
    def decorated_token(*args, **kwargs):

        if "login-token" in request.headers:
            token = request.headers['login-token']

        if not token:
            return jsonify({'msg':'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            user_curr = db.session.query(USER).filter(USER.UID == data['UID']).first()
        except:
            return jsonify({'msg': 'Token is not valid'}), 401
        return f(user_curr, *args, **kwargs)
    return decorated_token
#token_decoded = jwt.decode(jwt=token, key=app.config['SECRET_KEY'], algorithms="HS256")


@app.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        #querying db
        user = db.session.query(USER).filter(USER.U_NAME == data['name']).first()

        #does the user exist
        if user:

            #hash checking password
            if check_password_hash(user.PWORD, data['password']):
                token = jwt.encode({'UID': user.UID, 'PWORD': data['password'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
                '''
                #triggering the reminder thing
                global users_notvisited_notadmin
                users_notvisited_notadmin=trigger_daily_reminder_emails()'''
                return {'token': token, 'user_curr' : user.UID, 'admin':user.ADMIN}



            else:
                raise BusinessValidationError(status_code=401, error_message='Your password or possibly your username is wrong; pls fill them in correctly')

        return {'msg':'Your '}, 200
    #return token


@app.route('/sign_up', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()

        #creating and adding the new user to the database
        password_hashed = generate_password_hash(data['password'])
        new_user = USER(U_NAME=data['name'], PWORD=password_hashed, ADMIN=0, VISITED=0, EMAIL=data['email'] )
        db.session.add(new_user)
        db.session.commit()

        #sending em a token to log em in
        token = jwt.encode({'UID': new_user.UID, 'PWORD': data['password'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
        return {'token': token, 'user_curr': new_user.UID, 'admin': new_user.ADMIN}

@app.route('/all_shows_get')
@token_required
def all_shows_get(user_curr):
    data = SHOW.query.all()

    shows={}
    for show in data:
        shows[show.SID] = {}
        shows[show.SID]['SID'] = show.SID
        shows[show.SID]['SNAME'] = show.SNAME
        shows[show.SID]['PRICE'] = show.PRICE
        shows[show.SID]['RATING_AGG'] = show.RATING_AGG
        shows[show.SID]['SIMAGE_ID'] = show.SIMAGE_ID
        shows[show.SID]['S_DESCR'] = show.S_DESCR
        shows[show.SID]['TAGS'] = show.S_TAGS
        #shows[show.SID][''] = show.

    return jsonify(shows)

@app.route('/specific_shows_get', methods=['GET','POST'])
@token_required
def specific_shows_get(user_curr):
    if request.method == 'POST':
        data = request.get_json()

        # getting the search key, doing the search
        # should be a holwe bunch of validity hcecks to see that its a good msg, ignore for now
        search_key = data['search_val']
        results=SHOW.query.msearch(search_key)

        #assembling the results
        shows = {}
        for show in results:
            shows[show.SID] = {}
            shows[show.SID]['SID'] = show.SID
            shows[show.SID]['SNAME'] = show.SNAME
            shows[show.SID]['PRICE'] = show.PRICE
            shows[show.SID]['RATING_AGG'] = show.RATING_AGG
            shows[show.SID]['SIMAGE_ID'] = show.SIMAGE_ID
            shows[show.SID]['S_DESCR'] = show.S_DESCR
            shows[show.SID]['TAGS'] = show.S_TAGS

        return jsonify(shows)

@app.route('/your_shows_get')
@token_required
def your_shows_get(user_curr):
    command=text(f"select SHOW.SID, SNAME, PRICE, RATING_AGG, SIMAGE_ID, S_DESCR, S_TAGS from SHOW, CREATIONS where CREATIONS.SID=SHOW.SID and CREATIONS.UID={user_curr.UID}")
    data = db.session.execute(command)

    shows = {}
    for show in data:
        shows[show.SID] = {}
        shows[show.SID]['SID'] = show.SID
        shows[show.SID]['SNAME'] = show.SNAME
        shows[show.SID]['PRICE'] = show.PRICE
        shows[show.SID]['RATING_AGG'] = show.RATING_AGG
        shows[show.SID]['SIMAGE_ID'] = show.SIMAGE_ID
        shows[show.SID]['S_DESCR'] = show.S_DESCR
        shows[show.SID]['S_TAGS'] = show.S_TAGS

    return jsonify(shows)

@app.route('/show_post', methods = ['GET', 'POST'])
@token_required
def show_post(user_curr):
    if request.method == 'POST':

        data = request.get_json()

        if request.headers['action'] == 'create':
            print(data)
            #adding the show to the database
            new_show = SHOW(SNAME=data['name'], PRICE=data['price'], RATING_AGG='-1', S_DESCR=data['s_descr'], S_TAGS=data['s_tags'])
            db.session.add(new_show)

            #getting the show we just made
            show_made = db.session.query(SHOW).filter(SHOW.SNAME == data['name']).first()

            #updating the creations table to keep track of who made this
            new_creation = CREATIONS(UID=user_curr.UID, SID=show_made.SID)
            db.session.add(new_creation)
            db.session.commit()

            return {'msg':'you just made a show'}


        if request.headers['action'] == 'update':
            show = db.session.query(SHOW).filter(SHOW.SID == data['sid']).first()

            show.SNAME = data['name']
            show.PRICE = data['price']

            db.session.add(show)
            db.session.commit()

            return {'msg':'you just updated a show'}

        if request.headers['action'] == 'delete':

            #getting the show
            show = db.session.query(SHOW).filter(SHOW.SID == data['sid']).first()

            #getting the creation
            delete_creation_command = text(f"delete from CREATIONS where CREATIONS.UID={user_curr.UID} and CREATIONS.SID={show.SID}")
            db.session.execute(delete_creation_command)

            #nuking it all
            db.session.delete(show)
            db.session.commit()

            return {'msg':'you just nuked a theatre'}

        return 'something is wrong, we did not enter the update block'

@app.route('/theatre_post', methods = ['GET','POST'])
@token_required
def theatre_post(user_curr):
    if request.method == 'POST':

        data = request.get_json()
        #print(request.headers['action'])
        #validity cchecks to see if this is an admin & if anything else needs to be added


        if request.headers['action'] == 'create':
            #adding the theatre
            new_theatre = THEATRE(TNAME=data['name'], CAPACITY=data['capacity'], LOCATION=data['location'])
            db.session.add(new_theatre)
            db.session.commit()

            #getting the theatre we just made
            theatre_made = db.session.query(THEATRE).filter(THEATRE.TNAME == data['name']).first()

            #updating the creations theatre to keep track of who made this
            new_creation = CREATIONS(UID=user_curr.UID, TID=theatre_made.TID)
            db.session.add(new_creation)
            db.session.commit()

            return {'msg':'Congratulations, a new theatre has been made'}

        if request.headers['action'] == 'update':

            theatre = db.session.query(THEATRE).filter(THEATRE.TID==data['tid']).first()

            #print(data)
            #print(theatre.TID, theatre.TNAME, theatre.CAPACITY)

            theatre.TNAME = data['name']
            theatre.CAPACITY = data['capacity']
            theatre.LOCATION = data['location']

            db.session.add(theatre)
            db.session.commit()
            return {'msg':'Congrats, a theatre was edited tonight'}

        if request.headers['action'] == 'delete':

            #getting and nuking the theatre
            theatre = db.session.query(THEATRE).filter(THEATRE.TID == data['tid']).first()


            #db.session.delete(creation)
            delete_creation_command = text(f"delete from CREATIONS where CREATIONS.UID={user_curr.UID} and CREATIONS.TID={theatre.TID}")
            db.session.execute(delete_creation_command)
            db.session.delete(theatre)
            db.session.commit()

            return {'msg':"If you're reading this, a theatre was just deleted from the world this day, and all memory of it was erased as well"}

        print('I have heard their cry', user_curr.UID, data)
        return {'msg':'I have seen the oppression of my people, and have heard their cry'}


@app.route('/your_theatres_get', methods = ['GET'])
@token_required
def your_theatres_get(user_curr):
    command = text(f"select THEATRE.TID, TNAME, CAPACITY, LOCATION, TIMAGE_ID from THEATRE, CREATIONS where CREATIONS.TID=THEATRE.TID and CREATIONS.UID={user_curr.UID}")
    data = db.session.execute(command)

    #converting data to dictionary
    theatres = {}
    for theatre in data:
        theatres[theatre.TID] = {}
        theatres[theatre.TID]['TID'] = theatre.TID
        theatres[theatre.TID]['TNAME'] = theatre.TNAME
        theatres[theatre.TID]['CAPACITY'] = theatre.CAPACITY
        theatres[theatre.TID]['LOCATION'] = theatre.LOCATION
        theatres[theatre.TID]['TIMAGE_ID'] = theatre.TIMAGE_ID

    return jsonify(theatres)

@app.route('/all_theatres_get')
@token_required
def all_theatres_get(user_curr):

    #the query
    data = THEATRE.query.all()

    theatres = {}
    for theatre in data:
        theatres[theatre.TID] = {}
        theatres[theatre.TID]['TID'] = theatre.TID
        theatres[theatre.TID]['TNAME'] = theatre.TNAME
        theatres[theatre.TID]['CAPACITY'] = theatre.CAPACITY
        theatres[theatre.TID]['LOCATION'] = theatre.LOCATION
        theatres[theatre.TID]['TIMAGE_ID'] = theatre.TIMAGE_ID

    #print(theatres)
    return jsonify(theatres)

@app.route('/specific_theatres_get', methods = ['GET', 'POST'])
@token_required
def specific_theatres_get(user_curr):
    if request.method == 'POST':
        data = request.get_json()

        #getting the search key, doing the search
        # should be a holwe bunch of validity hcecks to see that its a good msg, ignore for now
        search_key=data['search_val']
        results = THEATRE.query.msearch(search_key)

        #assembling the results
        theatres = {}
        for theatre in results:
            theatres[theatre.TID] = {}
            theatres[theatre.TID]['TID'] = theatre.TID
            theatres[theatre.TID]['TNAME'] = theatre.TNAME
            theatres[theatre.TID]['CAPACITY'] = theatre.CAPACITY
            theatres[theatre.TID]['LOCATION'] = theatre.LOCATION
            theatres[theatre.TID]['TIMAGE_ID'] = theatre.TIMAGE_ID

        return jsonify(theatres)

@app.route('/bookings_post', methods = ['GET','POST'])
@token_required
def bookings_post(user_curr):
    data = request.get_json()

        #adding the booking
    AID_REAL =int(data['AID'])+1
    new_booking = BOOKINGS(AID = str(AID_REAL), UID = user_curr.UID, TICKETS = data['Tickets'], SID = data['SID'], TID = data['TID'])

    db.session.add(new_booking)

        #ensuring dedecting the tickets
    tickets = int(data['Tickets'])
    airing = db.session.query(AIRINGS).filter(AIRINGS.AID == str(AID_REAL)).first()

    new_vacancies = int(airing.VACANCIES) - tickets

    command = text(f"update AIRINGS set VACANCIES = {new_vacancies} where AID = {airing.AID}")
    db.session.execute(command)

    db.session.commit()
    return {'msg':'Gulag it took this long to make this work? Crikey'}

@app.route('/bookings_get')
@token_required
def bookings_get(user_curr):
    command = text(f"select BID, SNAME, U_NAME, TICKETS, TNAME, STRT_TIME, STOP_TIME, AIRINGS.DATE, SHOW.SID, THEATRE.TID from BOOKINGS, AIRINGS, SHOW, THEATRE, USER where BOOKINGS.AID = AIRINGS.AID and BOOKINGS.SID = SHOW.SID and BOOKINGS.TID = THEATRE.TID and BOOKINGS.UID = USER.UID and USER.UID = {user_curr.UID} and SHOW.SID = AIRINGS.SID")
    #select BID, SNAME, U_NAME, PRICE, RATING_AGG, STRT_TIME, STOP_TIME, VACANCIES, TNAME, SHOW.SID, THEATRE.TID, AIRINGS.DATE
    BOOKINGS = db.session.execute(command)

    bookings = {}
    for booking in BOOKINGS:
        bookings[booking.BID]= {}
        bookings[booking.BID]['SNAME']=booking.SNAME
        bookings[booking.BID]['U_NAME']=booking.U_NAME
        bookings[booking.BID]['TICKETS']=booking.TICKETS
        bookings[booking.BID]['TNAME']=booking.TNAME
        bookings[booking.BID]['STRT_TIME']=booking.STRT_TIME
        bookings[booking.BID]['STOP_TIME']=booking.STOP_TIME
        bookings[booking.BID]['DATE']=booking.DATE
        bookings[booking.BID]['TID']=booking.TID
        bookings[booking.BID]['SID']=booking.SID


    return (jsonify(bookings))

@app.route('/future_airings_get')
@token_required
def future_airings_get(user_curr):
    #pls note, mechanism to retreive shows acc date still not figured out, I pronounce that that shall be the next task.

    #retreiving all shows (for not all, we'll figure out time later)
    command = text(f"select AID, SNAME, PRICE, RATING_AGG, STRT_TIME, STOP_TIME, VACANCIES, TNAME, SHOW.SID, THEATRE.TID, AIRINGS.DATE from SHOW, AIRINGS,THEATRE where SHOW.SID = AIRINGS.SID and THEATRE.TID = AIRINGS.TID and AIRINGS.VACANCIES>0")
    AIRINGS = db.session.execute(command)

    #compiling all shows into a json object
    airings = {}
    date= str(datetime.datetime.utcnow()).split(' ')[0]
    for airing in AIRINGS:
        if airing.DATE >= date:
            #print(airing.SNAME, airing.PRICE, airing.RATING_AGG, airing.STRT_TIME, airing.STOP_TIME, airing.TNAME)
            airings[airing.AID] = {}
            airings[airing.AID]['AID'] = airing.AID
            airings[airing.AID]['SNAME']=airing.SNAME
            airings[airing.AID]['PRICE'] = airing.PRICE
            airings[airing.AID]['RATING_AGG'] = airing.RATING_AGG
            airings[airing.AID]['STRT_TIME'] = airing.STRT_TIME
            airings[airing.AID]['STOP_TIME'] = airing.STOP_TIME
            airings[airing.AID]['VACANCIES'] = airing.VACANCIES
            airings[airing.AID]['TNAME'] = airing.TNAME
            airings[airing.AID]['SID'] = airing.SID
            airings[airing.AID]['TID'] = airing.TID
            airings[airing.AID]['DATE'] = airing.DATE

    return (jsonify(airings))
    print({'token': 'this url lets the user witness all upcoming shows'})

@app.route('/your_airings_get')
@token_required
def your_airings_get(user_curr):
    # retreiving all shows (for not all, we'll figure out time later)
    command = text(f"select AIRINGS.AID, SNAME, PRICE, RATING_AGG, STRT_TIME, STOP_TIME, VACANCIES, TNAME, SHOW.SID, THEATRE.TID, AIRINGS.DATE from SHOW, AIRINGS,THEATRE, CREATIONS where SHOW.SID = AIRINGS.SID and THEATRE.TID = AIRINGS.TID and AIRINGS.AID=CREATIONS.AID and CREATIONS.UID={user_curr.UID}")
    AIRINGS = db.session.execute(command)

    # compiling all shows into a json object
    airings = {}
    date = str(datetime.datetime.utcnow()).split(' ')[0]
    for airing in AIRINGS:
        if airing.DATE >= date:
            # print(airing.SNAME, airing.PRICE, airing.RATING_AGG, airing.STRT_TIME, airing.STOP_TIME, airing.TNAME)
            airings[airing.AID] = {}
            airings[airing.AID]['AID'] = airing.AID
            airings[airing.AID]['SNAME'] = airing.SNAME
            airings[airing.AID]['PRICE'] = airing.PRICE
            airings[airing.AID]['RATING_AGG'] = airing.RATING_AGG
            airings[airing.AID]['STRT_TIME'] = airing.STRT_TIME
            airings[airing.AID]['STOP_TIME'] = airing.STOP_TIME
            airings[airing.AID]['TNAME'] = airing.TNAME
            airings[airing.AID]['SID'] = airing.SID
            airings[airing.AID]['TID'] = airing.TID
            airings[airing.AID]['DATE'] = airing.DATE

    #print(airings)
    return (jsonify(airings))

@app.route('/get_airings_date_tid', methods=['GET','POST'])
@token_required
def get_airings_date_tid(user_curr):

    if request.method == 'POST':
        data = request.get_json()

        command = text(f"select AID, SNAME, PRICE, RATING_AGG, STRT_TIME, STOP_TIME, VACANCIES, TNAME, SHOW.SID, THEATRE.TID, AIRINGS.DATE from SHOW, AIRINGS,THEATRE where SHOW.SID = AIRINGS.SID and THEATRE.TID = AIRINGS.TID and AIRINGS.DATE = '{data['date']}' and AIRINGS.TID = '{data['tid']}'")
        AIRINGS = db.session.execute(command)

        # compiling all shows into a json object
        airings = {}
        for airing in AIRINGS:
            # print(airing.SNAME, airing.PRICE, airing.RATING_AGG, airing.STRT_TIME, airing.STOP_TIME, airing.TNAME)
            airings[airing.AID] = {}
            airings[airing.AID]['SNAME'] = airing.SNAME
            airings[airing.AID]['PRICE'] = airing.PRICE
            airings[airing.AID]['RATING_AGG'] = airing.RATING_AGG
            airings[airing.AID]['STRT_TIME'] = airing.STRT_TIME
            airings[airing.AID]['STOP_TIME'] = airing.STOP_TIME
            airings[airing.AID]['TNAME'] = airing.TNAME
            airings[airing.AID]['SID'] = airing.SID
            airings[airing.AID]['TID'] = airing.TID
            airings[airing.AID]['DATE'] = airing.DATE

        return (jsonify(airings))

@app.route('/airings_post', methods = ['GET', 'POST'])
@token_required
def airings_post(user_curr):

    if request.method == 'POST':
        data = request.get_json()

        if request.headers['action']=='create':
            #getting the theatre
            theatre_specific = db.session.query(THEATRE).filter(THEATRE.TID == data['theatre_specific']).first()

            #creating & adding the airing
            new_airing = AIRINGS(SID=data['show_specific'], TID=data['theatre_specific'], DATE=data['date'], VACANCIES=theatre_specific.CAPACITY, STRT_TIME=data['strt_time'], STOP_TIME=data['stop_time'])
            db.session.add(new_airing)
            db.session.commit()


            #getting the airing back
            command = text(f"select AID from AIRINGS where AIRINGS.SID={data['show_specific']} and AIRINGS.TID={data['theatre_specific']} and AIRINGS.STRT_TIME='{data['strt_time']}' and AIRINGS.STOP_TIME='{data['stop_time']}' and AIRINGS.DATE='{data['date']}' ")
            airings = db.session.execute(command)

            #for - loop to get the aid
            aid = -1
            for airing in airings:
                aid = airing.AID
                break
            print(aid)

            #making the creation
            creation = CREATIONS(UID=user_curr.UID, AID=aid)
            db.session.add(creation)
            db.session.commit()

            return {'msg':'well...something sure did happen.'}

        if request.headers['action'] == 'update':
            #getting the airing
            airing = db.session.query(AIRINGS).filter(AIRINGS.AID == data['aid']).first()

            #updating the airing
            airing.SID=data['show_selected']
            airing.TID=data['theatre_selected']
            airing.DATE=data['date']
            airing.STRT_TIME=data['strt_time']
            airing.STOP_TIME=data['stop_time']

            db.session.add(airing)
            db.session.commit()

            return {'msg':'congrats, you successfully updated your airing'}

        if request.headers['action'] == 'delete':
            airing=db.session.query(AIRINGS).filter(AIRINGS.AID == data['aid']).first()

            #getting the reltd creation
            delete_creation_command = text(f"delete from CREATIONS where CREATIONS.UID={user_curr.UID} and CREATIONS.AID = {airing.AID}")
            db.session.execute(delete_creation_command)

            #deleting the airing
            db.session.delete(airing)
            db.session.commit()

            return {'msg':'the airing is no more'}

@app.route('/ratings_post', methods = ['GET', 'POST'])
@token_required
def ratings_post(user_curr):
    if request.method == 'POST':

        #getting the data
        data = request.get_json()

        #adding the new rating
        new_rating = RATINGS(UID=user_curr.UID, SID= data['SID'], RATING = data['rating'])
        db.session.add(new_rating)
        db.session.commit()

        #getting the show being rated
        show = db.session.query(SHOW).filter(SHOW.SID==data['SID']).first()

        #getting the avg ratings
        ratings = db.session.query(RATINGS).filter(RATINGS.SID==data['SID']).all()
        rating_avg = 0
        rating_sum=0
        rating_count=0
        for rating in ratings:
            rating_count+=1
            rating_sum += int(rating.RATING)
        rating_avg = rating_sum/rating_count
        #print(rating_avg)

        #updating the show
        show.RATING_AGG=rating_avg
        db.session.add(show)
        db.session.commit()

        return {'msg':'1st half is done'}

@app.route('/test_route', methods = ['GET', 'POST'])
def test_route():
    daily_email_reminder.delay()
    return'well we sure did trigger a task ey ol chap!'


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # call test
    sender.add_periodic_task(
        crontab(hour=21, minute=18),
        g_chat_webhook.s(),
        name = "period task"
    )


def trigger_daily_reminder_emails():
    # getting all users
    command = text(f"select UID, U_NAME, EMAIL from USER where USER.ADMIN = 0 and USER.VISITED = 0")
    USERS = db.session.execute(command)

    users = []
    for USER in USERS:
        user = {}
        user['UID'] = USER.UID
        user['U_NAME'] = USER.U_NAME
        user['EMAIL'] = USER.EMAIL
        users.append(user)

    return users
    # test_basic.delay()
    # g_chat_webhook.delay()
    #daily_email_reminder.delay(users)
    #return 'Theoretically we just triggered the emails'


