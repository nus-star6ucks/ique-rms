"""
Includes Mongo DB configuration and connection
"""
from mongoengine import *  # Mongo NoSQL

"""
Local Mongo DB
"""
# Connect to local Mongo DB
connect('ique')


# Mongo DB data model
class Reportdata(Document):
    report_id = IntField()
    data_type = StringField()
    store_id = IntField()
    unit = StringField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    data = DictField()


# print('$ Mongo created !! ')
