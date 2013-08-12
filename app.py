from flask import Flask, render_template, request, send_file, abort, redirect, make_response, url_for, jsonify
from pprint import pprint
import urlparse
from raven.contrib.flask import Sentry
from modules.database import *
from modules.forms import *


app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = 'yolomcswaggerton'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://webjobs:dezijohnson@localhost/webjobs'
app.config['SENTRY_DSN'] = 'http://aa64c0f6453848d5a5fdb756aa539cac:28846e2afb004b0883093beb4df11033@sentry.nwdesign.us/8'
sentry = Sentry(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET'])
def index():
    form = searchForm(csrf_enabled=False)
    form.search.data = request.args.get('search')
    form.excluded.data = request.args.get('excluded')
    form.include_body.data = request.args.get('include_body')
    posts = []

    if request.method == "GET" and form.search.data and form.validate:
        search = form.search.data
        excluded_terms = [' & !' + term for term in form.excluded.data.split()][::-1]
        exclusions = "".join(excluded_terms)

        if form.include_body.data:
            column_name = 'body_tsv'
        else:
            column_name = 'title_tsv'

        conn = engine.connect()
        query = """
            SELECT post_id FROM post WHERE %s @@ to_tsquery('''%s''%s');
        """ % (column_name, search, exclusions)

        result = conn.execute(query)

        for post in result.fetchall():
            post_id = post[0]
            post = Post.query.filter_by(post_id=post_id).first()
            posts.append(post)

    return render_template('index.html', form=form, posts=posts)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9020)
