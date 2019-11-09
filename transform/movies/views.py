from flask import Blueprint, render_template, jsonify, abort
import json
from objectpath import Tree

movies_bp = Blueprint('movies', __name__)


def getTree():
    with open('../files/GioMovies.json', 'r') as file:
        data = json.load(file)
    file.close()
    return Tree(data)


@movies_bp.route('/')
@movies_bp.route('/index')
def index():
    gio = getTree()
    querie = gio.execute('$..topic[@.instanceOf.topicRef.href is "#Filme"]')
    data = list(querie)
    return render_template("index.html", data=data)


@movies_bp.route('/movie/<id>')
def movie(id):
    gio = getTree()
    querie = gio.execute('$..topic[@.id is "%s"]' % id)
    data = list(querie)
    if len(data) == 1:
        return jsonify(data[0])
    else:
        abort(404)
