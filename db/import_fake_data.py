# This needs to be run as python -m db.import_fake_data
# from the project root with an activated venv
import json
import sys

from run import app

# Import database classes and SQLAlchamy instance
from db.models import Customer, Facility, Device, \
    Data, User, UserToFacility, Role, db


def create_item(db_class, request_json):
    # Creates a db entry with data from request_json,
    # schema from columns and db_class

    required_columns = db_class.required_columns()

    try:
        # TODO change to a list comprehension
        for column in required_columns:
            required_attribute = request_json.get(column)

            if required_attribute is not None:
                continue
            elif required_attribute is None:
                raise ValueError('A required attribute had a value of None')
    except KeyError as e:
        error_message = 'KeyError - reason %s was not found' % str(e)
        print(error_message)
    else:
        new_item = db_class.from_dict(request_json)

        with app.app_context():
            db.session.add(new_item)

            # TODO add a try catch for sqlalchemy errors
            db.session.commit()

    # TODO add a more descriptive message
    # TODO add a 201 status code to request
    return new_item


def stage_item(db_class, request_json):
    # Creates a db entry with data from request_json, does not commit to db
    # schema pulled from db_class

    required_columns = db_class.required_columns()

    try:
        # TODO change to a list comprehension
        for column in required_columns:
            required_attribute = request_json.get(column)

            if required_attribute is not None:
                continue
            elif required_attribute is None:
                print(column)
                raise ValueError('A required attribute had a value of None')
    except KeyError as e:
        error_message = 'KeyError - reason %s was not found' % str(e)
        print(error_message)
    else:
        new_item = db_class.from_dict(request_json)

    # TODO add a more descriptive message
    # TODO add a 201 status code to request
    return new_item


def parse_data(data):

    for customer in data['customers']:
        create_item(Customer, customer)

    for facility in data['facilities']:
        create_item(Facility, facility)

    for device in data['devices']:
        create_item(Device, device)

    for obj in data['sets']:

        with app.app_context():
            customer = stage_item(Customer, obj['customer'])
            db.session.add(customer)

            for facility in obj['facilities']:
                new_facility = stage_item(Facility, facility)
                db.session.add(new_facility)

                new_facility.customer = customer

                for device in obj['devices']:
                    if device['address'] == new_facility.address:
                        new_device = stage_item(Device, device)
                        db.session.add(new_device)

                        new_device.facility = new_facility
                    else:
                        continue

            # TODO add a try catch for sqlalchemy errors
            db.session.commit()


def load_data():
    # script_path should be the path to catalog/db

    path_to_json = 'db/fake_data.JSON'

    # good explenation of with http://effbot.org/zone/python-with-statement.htm
    with open(path_to_json) as fake_data:
        data = json.load(fake_data)

    return data


if __name__ == '__main__':
    parse_data(load_data())
