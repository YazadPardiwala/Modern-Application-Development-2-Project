from application.database import db
import os

class USER(db.Model): #contains all users
    __tablename__ = "USER"
    UID = db.Column(db.Integer, primary_key = True)
    U_NAME = db.Column(db.String, nullable = False, unique = True)
    PWORD = db.Column(db.String, nullable = False)
    ADMIN = db.Column(db.Integer, nullable = False, default = 0)
    VISITED = db.Column(db.Integer, nullable = False, default = 0)
    EMAIL = db.Column(db.String, nullable = False, unique = True)

class THEATRE(db.Model):   #contains all theatre detes
    __tablename__ = "THEATRE"
    __searchable__ = ['TNAME', 'LOCATION']
    TID = db.Column (db.Integer, primary_key = True)
    TNAME = db.Column(db.String, nullable = False, unique = True)
    CAPACITY = db.Column(db.Integer, nullable = False)
    LOCATION = db.Column(db.String, nullable = False)
    TIMAGE_ID = db.Column(db.String)

class SHOW(db.Model):    # contains all show detes
    __tablename__ = "SHOW"
    __searchable__ = ['SNAME','S_DESCR' , 'S_TAGS']
    SID = db.Column(db.Integer, primary_key = True)
    SNAME = db.Column(db.String, nullable=False, unique=True)
    PRICE = db.Column(db.Integer, nullable = False)
    RATING_AGG = db.Column(db.Integer, nullable = True)
    SIMAGE_ID = db.Column(db.String, unique = True)
    S_DESCR = db.Column(db.String, default=None)
    S_TAGS = db.Column(db.String, default=None)



class RATINGS(db.Model):     #contains all individual entries of users rating shows
    __tablename__ = "RATINGS"
    RID = db.Column(db.Integer, primary_key = True)
    SID = db.Column(db.Integer, db.ForeignKey("SHOW.SID"), nullable=False)
    UID = db.Column(db.Integer, db.ForeignKey("USER.UID"), nullable=False)
    RATING = db.Column(db.Integer, nullable=False)


class BOOKINGS(db.Model):          #contains all individual entries of users booking shows
    __tablename__ = "BOOKINGS"
    BID = db.Column(db.Integer, primary_key=True)
    AID = db.Column(db.Integer, db.ForeignKey("AIRINGS.AID"), nullable=False)
    UID = db.Column(db.Integer, db.ForeignKey("USER.UID"), nullable=False)
    TICKETS = db.Column(db.Integer, nullable=False)
    SID = db.Column(db.Integer, db.ForeignKey("SHOW.SID"), nullable=True)
    TID = db.Column(db.Integer, db.ForeignKey("THEATRE.TID"), nullable=True)


class AIRINGS(db.Model):           # contains all entries of a show airing at a certain time at a certain theatre
    __tablename__ = "AIRINGS"
    AID = db.Column(db.Integer, primary_key=True)
    SID = db.Column(db.Integer, db.ForeignKey("SHOW.SID"), nullable = False)
    TID = db.Column(db.Integer, db.ForeignKey("THEATRE.TID"), nullable = False)
    STRT_TIME = db.Column(db.String, nullable = False)
    STOP_TIME = db.Column(db.String, nullable = False)
    DATE = db.Column(db.String, nullable = False)
    VACANCIES = db.Column(db.Integer, nullable = False)


class CREATIONS(db.Model):      #which admin created what theatre/show/airing
    __tablename__ = "CREATIONS"
    CID = db.Column(db.Integer, primary_key=True)
    UID = db.Column(db.Integer, db.ForeignKey("USER.UID"), nullable=False )
    SID = db.Column(db.Integer, db.ForeignKey("SHOW.SID"), nullable=True)
    AID = db.Column(db.Integer, db.ForeignKey("AIRINGS.AID"), nullable=True)
    TID = db.Column(db.Integer, db.ForeignKey("THEATRE.TID"), nullable=True)



