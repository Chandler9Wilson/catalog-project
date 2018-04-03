import sys
import datetime

from flask_sqlalchemy import SQLAlchemy

# for why SQLAlchemy(app) is not called
# see https://stackoverflow.com/a/9695045/6879253
db = SQLAlchemy()


class Customer(db.Model):
    """The customer of a dealer

    The customer is the highest unit in the business data of this project.
    This means that excluding website data e.g. ``User``
    no unit will own a customer. Most customers will have a
    one to many relationship with ``Facility`` and by inheritence
    ``Device`` and ``Data``.

    Attributes:
        id (int): This is an automatically generated primary id this should
            never be modified by a user.
        name (str): This is the customer name e.g. Bowditch Navigation.
            This is a required attribute.
        facilities (list): A list of ``Facility`` objects with this customer
            instance as a foreign key. This is populated by sqlalchemy and is
            not a column in the database.
    """

    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # Begin sqlalchemy specific code (wont be in the db)

    facilities = db.relationship('Facility', back_populates='customer')

    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (
            self.id, self.name)

    # CRED https://stackoverflow.com/a/11884806/6879253
    def as_dict(self):
        """Returns an easily serializable dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def required_columns(cls):
        """Returns all required columns on the table.

        Looks specifically for required (nullable=False) columns
        excluding primary keys

        Returns:
            A list of column names that match the above spec e.g. ::

                [
                    'name'
                ]
        """
        # https://docs.python.org/3.5/tutorial/datastructures.html#list-comprehensions
        columns = [
            c.name for c in cls.__table__.columns if not c.nullable and not
            c.primary_key]
        return columns

    @classmethod
    def available_columns(cls):
        """Returns all user modifiable columns on the table.

        Looks specifically for available (nullable=False) columns
        excluding primary keys

        Returns:
            A list of column names that match the above spec e.g. ::

                [
                    'name'
                ]
        """
        # https://docs.python.org/3.5/tutorial/datastructures.html#list-comprehensions
        columns = [
            c.name for c in cls.__table__.columns if not c.primary_key]
        return columns

    # CRED https://stackoverflow.com/a/30114013/6879253
    @classmethod
    def from_dict(cls, d):
        """Creates a ``Customer`` from a dictionary

        Filters a given dictionary to a new dictionary containing
        only allowed fields, then passes this new dictionary to the
        class for creation.

        Args:
            d (dict): A dictionary with all primary keys filled in
                (this method does not filter for null or empty required keys)

        Returns:
            A new class instance created from the filtered dictionary.
        """
        allowed = cls.available_columns()

        # https://www.python.org/dev/peps/pep-0274/
        dict_filter = {key: value for key,
                       value in d.items() if key in allowed}

        return cls(**dict_filter)


class Facility(db.Model):
    """A building that has or will contain devices

    The ``Facility`` should usually be owned by a ``Customer``
    but this is not a requirement. It's also usual for a facility to have
    a one to many relationship with the ``Device`` table and
    by inheritance the ``Data`` table.

    Attributes:
        id (int): This is an automatically generated primary id this should
            never be modified by a user.
        address (str): The full form address of a facility. This will need
            to be prevalidated no validation is done within the class
            currently. This is a required attribute.
        customer_id (int): This should be the foreign key of a valid
            ``Customer``. This attribute is encouraged but optional.
        customer (obj): A customer that "owns" this facility. This is
            populated by sqlalchemy and is not a column in the database.
        devices (list): A list of ``Device`` instance objects with a foreign
            key of this facility. This is populated by sqlalchemy and is not
            a column in the database.
    """

    __tablename__ = 'facility'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id', ondelete='SET NULL'))

    # Begin sqlalchemy specific code (wont be in the db)

    customer = db.relationship('Customer', back_populates='facilities')
    devices = db.relationship('Device', back_populates='facility')

    def __repr__(self):
        return "<User(id='%s', address='%s', customer_id='%s')>" % (
            self.id, self.address, self.customer_id)

    # CRED https://stackoverflow.com/a/11884806/6879253
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def required_columns(cls):
        # returns all required (nullable=False) columns \
        # excluding primary key in a list

        # https://docs.python.org/3.5/tutorial/datastructures.html#list-comprehensions
        columns = [
            c.name for c in cls.__table__.columns if not c.nullable and not
            c.primary_key]
        return columns

    @classmethod
    def available_columns(cls):
        # returns all available columns excluding primary key in a list

        # https://docs.python.org/3.5/tutorial/datastructures.html#list-comprehensions
        columns = [
            c.name for c in cls.__table__.columns if not c.primary_key]
        return columns

    # CRED https://stackoverflow.com/a/30114013/6879253
    @classmethod
    def from_dict(cls, d):
        # allows the class to be created from a dict (d)

        allowed = cls.available_columns()

        dict_filter = {key: value for key,
                       value in d.items() if key in allowed}

        return cls(**dict_filter)


class Device(db.Model):

    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    hardware_id = db.Column(db.String, nullable=False)
    device_type = db.Column(db.String, nullable=False)
    hvac_description = db.Column(db.String)
    facility_id = db.Column(db.Integer, db.ForeignKey(
        'facility.id', ondelete='SET NULL'))

    # Begin sqlalchemy specific code (wont be in the db)

    data = db.relationship('Data', back_populates='device')
    facility = db.relationship('Facility', back_populates='devices')

    def __repr__(self):
        return """<User(id='%s', hardware_id='%s', device_type='%s',
            hvac_description='%s', facility_id='%s')>""" % (
            self.id, self.hardware_id, self.device_type,
            self.hvac_description, self.facility_id)

    # CRED https://stackoverflow.com/a/11884806/6879253
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def required_columns(cls):
        # returns all required (nullable=False) columns \
        # excluding primary key in a list

        # https://docs.python.org/3.5/tutorial/datastructures.html#list-comprehensions
        columns = [
            c.name for c in cls.__table__.columns if not c.nullable and not
            c.primary_key]
        return columns

    @classmethod
    def available_columns(cls):
        # returns all available columns excluding primary key in a list

        # https://docs.python.org/3.5/tutorial/datastructures.html#list-comprehensions
        columns = [
            c.name for c in cls.__table__.columns if not c.primary_key]
        return columns

    # CRED https://stackoverflow.com/a/30114013/6879253
    @classmethod
    def from_dict(cls, d):
        # allows the class to be created from a dict (d)

        allowed = cls.available_columns()

        dict_filter = {key: value for key,
                       value in d.items() if key in allowed}

        return cls(**dict_filter)


class Data(db.Model):
    # Reguraly collected data, will be constantly hit with updates

    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    t1 = db.Column(db.Float)
    t2 = db.Column(db.Float)
    t3 = db.Column(db.Float)
    power = db.Column(db.Float)
    operation = db.Column(db.String(4))
    fan_on = db.Column(db.Boolean)
    device_id = db.Column(db.Integer, db.ForeignKey(
        'device.id', ondelete='SET NULL'))

    # Begin sqlalchemy specific code (wont be in the db)

    device = db.relationship('Device', back_populates='data')

    def __repr__(self):
        return """<User(id='%s', timestamp='%s', t1='%s', t2='%s', t3='%s',
            power='%s', operation='%s', fan_on='%s',
            device_id='%s')>""" % (
            self.id, self.timestamp, self.t1, self.t2, self.t3, self.power,
            self.operation, self.fan_on, self.device_id)

    # CRED https://stackoverflow.com/a/11884806/6879253
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def required_columns(cls):
        # returns all required (nullable=False) columns \
        # excluding primary key in a list

        # https://docs.python.org/3.5/tutorial/datastructures.html#list-comprehensions
        columns = [
            c.name for c in cls.__table__.columns if not c.nullable and not
            c.primary_key]
        return columns

    @classmethod
    def available_columns(cls):
        # returns all available columns excluding primary key in a list

        # https://docs.python.org/3.5/tutorial/datastructures.html#list-comprehensions
        columns = [
            c.name for c in cls.__table__.columns if not c.primary_key]
        return columns

    # CRED https://stackoverflow.com/a/30114013/6879253
    @classmethod
    def from_dict(cls, d):
        # allows the class to be created from a dict (d)

        allowed = cls.available_columns()

        dict_filter = {key: value for key,
                       value in d.items() if key in allowed}

        return cls(**dict_filter)


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

    def __init__(self, email, oauth_provider, active=True):
        self.oauth_provider = oauth_provider
        self.email = email
        self.is_active = active

    def __repr__(self):
        return """<User(id='%s', name='%s', email='%s', profile_pic='%s',
            oauth_provider='%s')>""" % (
            self.id, self.name, self.email, self.profile_pic,
            self.oauth_provider)

    def is_authenticated(self):
        return True

    def is_active(self):
        # this needs to be changed to accomadate a deactivated user
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @classmethod
    def required_columns(cls):
        # returns all required (nullable=False) columns \
        # excluding primary key in a list

        # https://docs.python.org/3.5/tutorial/datastructures.html#list-comprehensions
        columns = [
            c.name for c in cls.__table__.columns if not c.nullable and not
            c.primary_key]
        return columns

    @classmethod
    def available_columns(cls):
        # returns all available columns excluding primary key in a list

        # https://docs.python.org/3.5/tutorial/datastructures.html#list-comprehensions
        columns = [
            c.name for c in cls.__table__.columns if not c.primary_key]
        return columns


class UserToFacility(db.Model):
    # A workers db.relationship to a facility to be used with permissions

    __tablename__ = 'user_to_facility'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'))

    # Begin sqlalchemy specific code (wont be in the db)

    user = db.relationship('User')
    facility = db.relationship('Facility')

    def __repr__(self):
        return "<User(id='%s', user_id='%s', facility_id='%s')>" % (
            self.id, self.user_id, self.facility_id)

    @classmethod
    def required_columns(cls):
        # returns all required (nullable=False) columns \
        # excluding primary key in a list

        # https://docs.python.org/3.5/tutorial/datastructures.html#list-comprehensions
        columns = [
            c.name for c in cls.__table__.columns if not c.nullable and not
            c.primary_key]
        return columns

    @classmethod
    def available_columns(cls):
        # returns all available columns excluding primary key in a list

        # https://docs.python.org/3.5/tutorial/datastructures.html#list-comprehensions
        columns = [
            c.name for c in cls.__table__.columns if not c.primary_key]
        return columns


class Role(db.Model):
    # A users Role e.g. contracter, admin
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Begin sqlalchemy specific code (wont be in the db)

    user = db.relationship('User')

    def __repr__(self):
        return "<User(id='%s', title='%s', user_id='%s')>" % (
            self.id, self.title, self.user_id)

    @classmethod
    def required_columns(cls):
        # returns all required (nullable=False) columns \
        # excluding primary key in a list

        # https://docs.python.org/3.5/tutorial/datastructures.html#list-comprehensions
        columns = [
            c.name for c in cls.__table__.columns if not c.nullable and not
            c.primary_key]
        return columns

    @classmethod
    def available_columns(cls):
        # returns all available columns excluding primary key in a list

        # https://docs.python.org/3.5/tutorial/datastructures.html#list-comprehensions
        columns = [
            c.name for c in cls.__table__.columns if not c.primary_key]
        return columns
