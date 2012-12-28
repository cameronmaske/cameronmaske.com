#Based on this tutorial - https://nicolas.perriault.net/code/2012/dead-easy-yet-powerful-static-website-generator-with-flask/
import sys

from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)


#The homepage: e.g. cameronmaske.com/
@app.route('/')
def index():
    return render_template('index.html', pages=pages)


#Individual blog articles. e.g. cameronmaske.com/what-is-wrong-with-the-world
@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('post.html', page=page)

if __name__ == '__main__':
    # $ python builder.py build : generates the static site.
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    # $ python builder.py : serves the site locally for dev.e
    else:
        app.run(port=8000)
