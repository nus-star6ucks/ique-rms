from flask import Flask

app = Flask(__name__)


@app.route('/v1/python')
def hello():
    return '[Python Flask] Hello, World!'
