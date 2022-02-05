from datetime import datetime
from flaskApp import db
from flask_login import UserMixin



class Student(db.Model):
    __tablename__ = 'students'
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(40))
    lname=db.Column(db.String(40))
    email=db.Column(db.String(40))

    # def __repr__(self):
    #     return f"Student('{self.fname}', '{self.lname}', '{self.email}')"
    def __init__(self,fname,lname,email):
        self.fname=fname
        self.lname=lname
        self.email=email