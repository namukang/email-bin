from gevent import monkey; monkey.patch_all()
from gevent.wsgi import WSGIServer

import os, datetime, urlparse, re
import logging
logging.basicConfig()

from pymongo import Connection
from flask import Flask, request, Response

from access_control import crossdomain

EMAIL_REGEX = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}')
# domains allowed to invoke the XMLHttpRequest API
ALLOWED_DOMAINS = ['*']

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
@crossdomain(origin=ALLOWED_DOMAINS)
def signup():
    email = request.form['email']
    if email and re.match(EMAIL_REGEX, email):
        signup = {
                'email': email,
                'ip': request.access_route[0],
                'time': datetime.datetime.utcnow(),
                }
        app.database.signups.insert(signup)
        return Response("Thanks for signing up!", status=201)
    else:
        return Response("Sorry, your email address is invalid.", status=400)

def connect_to_db():
    """Connect to database"""
    MONGOLAB_URI = os.environ['MONGOLAB_URI']
    MONGODB_HOST = urlparse.urlparse(MONGOLAB_URI).geturl()
    MONGODB_PORT = urlparse.urlparse(MONGOLAB_URI).port
    DATABASE_NAME = urlparse.urlparse(MONGOLAB_URI).path[1:]

    connection = Connection(MONGODB_HOST, MONGODB_PORT)
    app.database = connection[DATABASE_NAME]

if __name__ == '__main__':
    connect_to_db()
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()
