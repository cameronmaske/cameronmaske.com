# Based on this tutorial
# https://nicolas.perriault.net/code/2012/dead-easy-yet-powerful-static-website-generator-with-flask/

import sys
import shutil
import os

from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

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
        articles = (p for p in pages if 'date' in p.meta)
    # Else, display only published ones.
    else:
        articles = (p for p in pages if 'published' and 'date' in p.meta)
    # Show the 10 most recent articles, most recent first.
    print articles
    articles = sorted(articles, reverse=True, key=lambda p: p.meta['date'])
    return render_template('index.html', articles=articles)


# Individual blog articles. e.g. cameronmaske.com/what-is-wrong-with-the-world
@app.route('/<path:path>/')
def page(path):
    article = pages.get_or_404(path)
    return render_template('post.html', article=article)

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
