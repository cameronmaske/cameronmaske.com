# Based on this tutorial
# https://nicolas.perriault.net/code/2012/dead-easy-yet-powerful-static-website-generator-with-flask/

import sys
import shutil
import os

from flask import Flask, render_template, request, make_response
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from werkzeug.contrib.atom import AtomFeed

from deploy import Site

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FREEZER_DESTINATION = '.build'

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)


#The homepage: e.g. cameronmaske.com/
@app.route('/')
def index():
    # If in debug, show all articles.
    if DEBUG:
        articles = (p for p in pages)
    # Else, display only published ones.
    else:
        articles = (p for p in pages if 'published' in p.meta)
    # Show the 10 most recent articles, most recent first.
    articles = sorted(articles, reverse=True, key=lambda p: p.meta['date'])
    return render_template('index.html', articles=articles)


# Individual blog articles. e.g. cameronmaske.com/what-is-wrong-with-the-world
@app.route('/<path:path>/')
def page(path):
    article = pages.get_or_404(path)
    return render_template('post.html', article=article)


# Sitemap XML. Seo goodness!
@app.route('/sitemap.xml')
def sitemap():
    articles = (p for p in pages if 'published' in p.meta)
    response = make_response(render_template('sitemap.xml', articles=articles))
    response.headers['Content-Type'] = 'application/xml'
    return response


@app.route('/feed.atom')
def recent_feed():
    feed = AtomFeed('Recent Articles',
                    feed_url=request.url, url=request.url_root)

    articles = (p for p in pages if 'published' in p.meta)

    for article in articles:
        feed.add(article['title'], unicode(article.html),
                 content_type='html',
                 url=article.path,
                 author='Cameron Maske',
                 published=article['date'],
                 updated=article['date'])
    return feed.get_response()

if __name__ == '__main__':
    # $ python builder.py build : generates the static site.
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        DEBUG = False
        freezer.freeze()
        shutil.rmtree('.build/static/less')  # Remove less files.
        shutil.rmtree('.build/static/coffee')  # Remove coffee files.
    # $ python builder.py deploy : pushes the site to S3
    elif len(sys.argv) > 1 and sys.argv[1] == 'deploy':
        print('Starting to deploy...\n')
        site = Site(os.getcwd())
        #site.verify()
        site.upload()
    # $ python builder.py : serves the site locally for dev.e
    else:
        app.run(port=8000)
