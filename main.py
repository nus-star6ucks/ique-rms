import functions_framework
import os
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
import pymysql

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './_key.json'

# os.environ.se


# auth.authenticate_user()

# initialize Connector object
connector = Connector()


# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "ique-star6ucks:asia-southeast1:queue-db",
        "pymysql",
        user="queue-manager",
        password="rTJBMdkj6LrCSf0+",
        db="zoe",
        ip_type=IPTypes.PUBLIC,
        enable_iam_auth=False
    )
    return conn


# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# interact with Cloud SQL database using connection pool
with pool.connect() as db_conn:
    print('** gcloud DB : connect successfully!')
    # query database
    result = db_conn.execute("SELECT * from my_table").fetchall()

connector.close()


# [START functions_helloworld_get]

@functions_framework.http
def hello_get(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    Note:
        For more information on how Flask integrates with Cloud
        Functions, see the `Writing HTTP functions` page.
        <https://cloud.google.com/functions/docs/writing/http#http_frameworks>
    """
    return 'Hello World!!!!'

# [END functions_helloworld_get]

# [END functions_helloworld_http]
