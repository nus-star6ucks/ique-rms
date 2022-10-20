"""
Includes Postgres DB configuration and connection
"""
import datetime
from peewee import *
from playhouse.postgres_ext import *  # Postgres SQL Extension

"""
Local Postgres DB
"""
# Connect to local Postgres DB
# DB name & user name
pgdb = PostgresqlExtDatabase('ique', user='zoe')


# pg DB model
class BaseModel(Model):
    class Meta:
        database = pgdb


# create pg table model
class Store(BaseModel):
    store_id = IdentityField()
    name = TextField()
    register_time = DateTimeField(default=datetime.datetime.now)
    # register_time = TimestampField()
    # seatTypes = ArrayField(ForeignKeyField(seatType))
    merchant_id = IntegerField()


class Seattype(BaseModel):
    seattype_id = IdentityField()
    name = TextField()
    store_id = ForeignKeyField(Store)


# create DB data model
class Ticket(BaseModel):
    ticket_id = IdentityField()
    start_time = DateTimeField(default=datetime.datetime.now)
    end_time = DateTimeField(default=datetime.datetime.now)
    status = TextField()
    # start_time = TimestampField()
    # end_time = TimestampField()
    store_id = ForeignKeyField(Store)
    seattype_id = ForeignKeyField(Seattype)


class Report(BaseModel):
    report_id = IdentityField()  # DB created automatically
    store_id = IntegerField()
    merchant_id = IntegerField()
    type = TextField()
    unit = TextField()
    create_time = DateTimeField(default=datetime.datetime.now)  # year-month-day hour-minute-second
    url = TextField()


# connect to Postgres DB
pgdb.connect()
pgdb.create_tables([Store, Ticket, Seattype, Report])
# print('$ Postgres created !! ')

