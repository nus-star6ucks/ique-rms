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
pgdb = PostgresqlExtDatabase(
    'ique', user='ums', password="&2ZxqMQF'2{fQT}b", unix_socket='/cloudsql/ique-star6ucks:asia-southeast1:iqueue')

mysqldb = MySQLDatabase('qms',  user='queue-manager',
                        password="rTJBMdkj6LrCSf0+", unix_socket='/cloudsql/ique-star6ucks:asia-southeast1:queue-db')

# pg DB model


class PgBaseModel(Model):
    class Meta:
        database = pgdb


class MySqlBaseModel(Model):
    class Meta:
        database = mysqldb

# create pg table model


class Store(PgBaseModel):
    class Meta:
        table_name = 'store'
    id = BigIntegerField()
    name = TextField()
    register_time = BigIntegerField()
    # register_time = TimestampField()
    # seatTypes = ArrayField(ForeignKeyField(seatType))
    merchant_id = BigIntegerField()


class Seattype(PgBaseModel):
    class Meta:
        table_name = 'store_seat_types'
    id = BigIntegerField()
    name = TextField()
    store_id = BigIntegerField()


# create DB data model
class Ticket(MySqlBaseModel):
    class Meta:
        table_name = 'queue_ticket'

    ticket_id = BigIntegerField()
    start_time = BigIntegerField()
    end_time = BigIntegerField()
    status = TextField()
    # start_time = TimestampField()
    # end_time = TimestampField()
    store_id = BigIntegerField()


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

pgdb.create_tables([Report])
