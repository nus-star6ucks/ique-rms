"""
Includes Postgres DB configuration and connection
"""
import datetime
from peewee import *
from playhouse.postgres_ext import *  # Postgres SQL Extension

"""
GCloud Postgres DB
"""
# Connect to gcloud Postgres DB
# DB name & user name
pgdb = PostgresqlExtDatabase('ique', user='ums')

mysqldb = MySQLDatabase('qms')

# pg DB model


class PgBaseModel(Model):
    class Meta:
        database = pgdb


class MySqlBaseModel(Model):
    class Meta:
        database = mysqldb

# create pg table model


class Store(PgBaseModel):
    id = BigIntegerField()
    name = TextField()
    register_time = DateTimeField(default=datetime.datetime.now)
    # register_time = TimestampField()
    # seatTypes = ArrayField(ForeignKeyField(seatType))
    merchant_id = BigIntegerField()


class Seattype(PgBaseModel):
    id = BigIntegerField()
    name = TextField()
    store_id = BigIntegerField()


# create DB data model
class Ticket(MySqlBaseModel):
    ticket_id = IdentityField()
    start_time = DateTimeField(default=datetime.datetime.now)
    end_time = DateTimeField(default=datetime.datetime.now)
    status = TextField()
    # start_time = TimestampField()
    # end_time = TimestampField()
    store_id = ForeignKeyField(Store)
    seattype_id = ForeignKeyField(Seattype)


class Report(PgBaseModel):
    report_id = IdentityField()  # DB created automatically
    store_id = IntegerField()
    merchant_id = IntegerField()
    type = TextField()
    unit = TextField()
    # year-month-day hour-minute-second
    create_time = DateTimeField(default=datetime.datetime.now)
    url = TextField()


pgdb.connect()
mysqldb.connect()