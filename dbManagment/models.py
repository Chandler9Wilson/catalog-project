import sys
import datetime

from flask_sqlalchemy import SQLAlchemy

# for why SQLAlchemy(app) is not called
# see https://stackoverflow.com/a/9695045/6879253
db = SQLAlchemy()


class Customer(db.Model):

    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class Facility(db.Model):

    __tablename__ = 'facility'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship(Customer)


class Device(db.Model):

    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    device_type = db.Column(db.String, nullable=False)
    location_description = db.Column(db.String)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'))
    facility = db.relationship(Facility)


class Data(db.Model):
    # Reguraly collected data will be constantly hit with updates

    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    t1 = db.Column(db.Float)
    t2 = db.Column(db.Float)
    t3 = db.Column(db.Float)
    power = db.Column(db.Float)
    operation = db.Column(db.String(4), nullable=False)
    fan_on = db.Column(db.Boolean, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    device = db.relationship(Device)


# Start user related tables


class User(db.Model):
    # A user of the website

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False)
    profile_pic = db.Column(db.String)
    # TODO this needs to be a seperate table
    # for multiple login options for the same user
    oauth_provider = db.Column(db.String, nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        # this needs to be changed to accomadate a deactivated user
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class UserToFacility(db.Model):
    # A workers db.relationship to a facility to be used with permissions

    __tablename__ = 'user_to_facility'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'))
    facility = db.relationship(Facility)


class Role(db.Model):
    # This design might need a revision currently
    # a join will be needed everytime a role is pulled

    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
