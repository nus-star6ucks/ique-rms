"""
Includes Postgres DB configuration and connection
"""
import sqlalchemy  # Postgres SQL Extension
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
import os


"""
GCloud Postgres DB
"""
# Connect to gcloud Postgres DB

mysqldb = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username=os.environ['DB_MYSQL_USER'],
        password=os.environ['DB_MYSQL_PASS'],
        database=os.environ['DB_MYSQL_NAME'],
        query=dict(
            {"unix_socket": os.environ['DB_MYSQL_UNIX_SOCKET'] }),
    ),
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800
)

pgdb = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername="postgresql+psycopg2",
        username=os.environ['DB_PG_USER'],
        password=os.environ['DB_PG_PASS'],
        database=os.environ['DB_PG_NAME'],
        host=os.environ['DB_PG_UNIX_SOCKET']
    ),
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800
)


Base = declarative_base()


class Store(Base):
    __tablename__ = 'store'

    id = Column(sqlalchemy.BigInteger, primary_key=True)
    name = Column(sqlalchemy.String)
    register_time = Column(sqlalchemy.BigInteger)
    merchant_id = Column(sqlalchemy.BigInteger)

    def __init__(self, name, register_time, merchant_id):
        self.name = name
        self.register_time = register_time
        self.merchant_id = merchant_id


class Seattype(Base):
    __tablename__ = 'store_seat_types'

    id = Column(sqlalchemy.BigInteger, primary_key=True)
    name = Column(sqlalchemy.String)
    store_id = Column(sqlalchemy.BigInteger)

    def __init__(self, name, register_time, store_id):
        self.name = name
        self.register_time = register_time
        self.store_id = store_id


class Ticket(Base):
    __tablename__ = 'queue_ticket'

    ticket_id = Column(sqlalchemy.BigInteger, primary_key=True)
    start_time = Column(sqlalchemy.BigInteger)
    end_time = Column(sqlalchemy.BigInteger)
    status = Column(sqlalchemy.String)
    store_id = Column(sqlalchemy.BigInteger)

    def __init__(self, ticket_id, start_time, end_time, status, store_id):
        self.ticket_id = ticket_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.store_id = store_id


class Report(Base):
    __tablename__ = 'report'

    report_id = Column(sqlalchemy.BigInteger, primary_key=True)
    store_id = Column(sqlalchemy.BigInteger)
    merchant_id = Column(sqlalchemy.BigInteger)

    type = Column(sqlalchemy.String)
    unit = Column(sqlalchemy.String)

    create_time = Column(sqlalchemy.DateTime)
    url = Column(sqlalchemy.String)

    def __init__(self, store_id, merchant_id, type, unit, create_time, url):
        self.store_id = store_id
        self.merchant_id = merchant_id
        self.type = type
        self.unit = unit
        self.create_time = create_time
        self.url = url

pgdb.connect()
mysqldb.connect()
