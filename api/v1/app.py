#!/usr/bin/python3
"""My Flask Application"""
from flask import Flask
from models import storage
from models import *
from api.v1.views.__init__ import app_views
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_app(error):
    """Tear down the current session"""
    storage.close()




if __name__ == '__main__':
    try:
        host = getenv(HBNB_API_HOST)
        port = getenv(HBNB_API_PORT)
    except NameError:
        host = '0.0.0.0'
        port = 5000

    app.run(host=host, port=port, threaded=True)
