# """
# Includes Google Cloud DB configuration and connection
# """
# import pymysql
# import sqlalchemy
# from google.cloud.sql.connector import Connector, IPTypes

# """
# Google cloud MySQL
# """
# # initialize Connector object
# connector = Connector()


# # function to return the database connection
# def getconn() -> pymysql.connections.Connection:
#     conn: pymysql.connections.Connection = connector.connect(
#         "ique-star6ucks:asia-southeast1:queue-db",
#         "pymysql",
#         user="queue-manager",
#         password="rTJBMdkj6LrCSf0+",
#         db="zoe",
#         ip_type=IPTypes.PUBLIC,
#         enable_iam_auth=False
#     )
#     return conn


# # create connection pool
# pool = sqlalchemy.create_engine(
#     "mysql+pymysql://",
#     creator=getconn,
# )

# """
# # interact with Cloud SQL database using connection pool
# with pool.connect() as db_conn:
#     print('** gcloud DB : connect successfully!')
#     # query database
#     result = db_conn.execute("SELECT * from my_table").fetchall()
# """
# connector.close()