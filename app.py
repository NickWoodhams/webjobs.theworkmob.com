from flask import Flask, render_template, request, send_file, abort, redirect, make_response, url_for, jsonify
from pprint import pprint
import urlparse
from raven.contrib.flask import Sentry
from modules.database import *
from modules.forms import *


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'yolomcswaggerton'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://webjobs:dezijohnson@localhost/webjobs'
app.config['SENTRY_DSN'] = 'http://aa64c0f6453848d5a5fdb756aa539cac:28846e2afb004b0883093beb4df11033@sentry.nwdesign.us/8'
sentry = Sentry(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET'])
def index():
    form = searchForm()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9020)
