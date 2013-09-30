# -*- coding: utf-8 -*-
"""
    webjobs
    ~~~~~~~~

    craigslist scraper, web jobs search
"""

from flask import Flask, render_template, request, send_file, abort, redirect, make_response, url_for, jsonify
from pprint import pprint
import urlparse
from config import app
from modules.database import *
from modules.forms import *
from modules.functions import *


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
            SELECT * FROM post WHERE %s @@ to_tsquery('''%s''%s') AND timestamp > current_timestamp - interval '31 days' ORDER BY timestamp DESC;
        """ % (column_name, search, exclusions)

        result = conn.execute(query)

        for post in result.fetchall():
            post = dict(zip(post.keys(), post.values()))
            posts.append(post)

    return render_template('index.html', form=form, posts=posts)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9020)
