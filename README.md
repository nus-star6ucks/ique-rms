# Deploy a function to Cloud Run

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

This guide will show you how to deploy the following example function to [Cloud Run](https://cloud.google.com/run):

```python
def hello(request):
    return "Hello world!"
```

This guide assumes your Python function is defined in a `main.py` file and dependencies are specified in `requirements.txt` file.

## Running your function in a container

To run your function in a container, create a `Dockerfile` with the following contents:

```Dockerfile
# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY cloud_run_http .

# Install production dependencies.
RUN pip install functions-framework
RUN pip install -r requirements.txt

# Run the web service on container startup.
# YOUR_FUNCTION_NAME = Replace YOUR_FUNCTION_NAME with your function's method name
CMD exec functions-framework --target=YOUR_FUNCTION_NAME
```

Start the container locally by running `docker build` and `docker run`:

```sh
docker build -t helloworld . && docker run --rm -p 8080:8080 -e PORT=8080 helloworld
```

Send requests to this function using `curl` from another terminal window:

```sh
curl localhost:8080
# Output: Hello world!
```

## Configure gcloud

To use Docker with gcloud, [configure the Docker credential helper](https://cloud.google.com/container-registry/docs/advanced-authentication):

```sh
gcloud auth configure-docker
```

## Deploy a Container

You can deploy your containerized function to Cloud Run by following the [Cloud Run quickstart](https://cloud.google.com/run/docs/quickstarts/build-and-deploy).

Use the `docker` and `gcloud` CLIs to build and deploy a container to Cloud Run, replacing `[PROJECT-ID]` with the project id and `helloworld` with a different image name if necessary:

```sh
docker build -t gcr.io/[PROJECT-ID]/helloworld .
docker push gcr.io/[PROJECT-ID]/helloworld
gcloud run deploy helloworld --image gcr.io/[PROJECT-ID]/helloworld --region us-central1
```

If you want even more control over the environment, you can [deploy your container image to Cloud Run on GKE](https://cloud.google.com/run/docs/quickstarts/prebuilt-deploy-gke). With Cloud Run on GKE, you can run your function on a GKE cluster, which gives you additional control over the environment (including use of GPU-based instances, longer timeouts and more).

# Connect to Gcloud MySQL

[GoogleCloudPlatform : cloud-sql-python-connector](https://github.com/GoogleCloudPlatform/cloud-sql-python-connector)

```python
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
```

## IAM

1. Add principles role
   1. Cloud SQL Admin
   2. Cloud SQL Client
![](../../../../../../../../../var/folders/69/p0sgjx_x06g3dps3xb05kq7r0000gn/T/TemporaryItems/NSIRD_screencaptureui_y8EztU/截屏2022-10-04 22.01.32.png)


2. Create service account 
![](../../../../../../../../../var/folders/69/p0sgjx_x06g3dps3xb05kq7r0000gn/T/TemporaryItems/NSIRD_screencaptureui_S3VzQj/截屏2022-10-04 22.05.02.png)


3. Generate KEY and Download Key.json file
![](../../../../../../../../../var/folders/69/p0sgjx_x06g3dps3xb05kq7r0000gn/T/TemporaryItems/NSIRD_screencaptureui_jShWNy/截屏2022-10-04 22.05.18.png)


4. Move Key.json file to project file
![](../../../../../../../../../var/folders/69/p0sgjx_x06g3dps3xb05kq7r0000gn/T/TemporaryItems/NSIRD_screencaptureui_Q7eOz8/截屏2022-10-04 22.06.38.png)


5. Add environment into code
```python
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './_key.json'
```

## Create DB 
6. Create new DB in Cloud SQL instance
![](../../../../../../../../../var/folders/69/p0sgjx_x06g3dps3xb05kq7r0000gn/T/TemporaryItems/NSIRD_screencaptureui_pz6GMV/截屏2022-10-04 22.10.34.png)


## Connection
7. Set connection information
```python
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
```
