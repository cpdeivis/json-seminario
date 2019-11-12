from flask import Blueprint, render_template, jsonify, abort
import json
from objectpath import Tree

movies_bp = Blueprint('movies', __name__)


# UTILS
def getTree():
    with open('../files/GioMovies.json', 'r') as file:
        data = json.load(file)
    file.close()
    return Tree(data)


def getBaseName(id, tree):
    querie = tree.execute('$..topic[@.id is "%s"]' % id.replace('#', ''))
    data = list(querie)[0]
    if len(data['baseName']) > 1:
        return data['baseName'][0]['baseNameString']
    return data['baseName']['baseNameString']


# end UTILS

@movies_bp.route('/')
@movies_bp.route('/index')
def index():
    gio = getTree()
    querie = gio.execute('$..topic[@.instanceOf.topicRef.href is "#Filme"]')
    data = list(querie)
    return render_template("index.html", data=data)


@movies_bp.route('/movies/<id>')
def movies(id):
    gio = getTree()
    querie = gio.execute('$..topic[@.id is "%s"]' % id)
    data = list(querie)
    if len(data) == 1:
        data = data[0]
        for ocr in data['occurrence']:
            if 'scope' in ocr:
                ocr['scope'] = getBaseName(ocr['scope']['topicRef']['href'], gio)
            elif 'instanceOf' in ocr:
                ocr['scope'] = getBaseName(ocr['instanceOf']['topicRef']['href'], gio)
                ocr['resourceData'] = ocr['resourceRef']['href']
                del ocr['instanceOf']
                del ocr['resourceRef']

        querie = gio.execute('$..association["#%s" in @.member..href]' % id)
        association = list(querie)
        for ass in association:
            ass['instanceOf'] = getBaseName(ass['instanceOf']['topicRef']['href'], gio)
            member = list(filter(lambda x: x['topicRef']['href'] != ('#' + id), ass['member']))[0]
            ass['member'] = {'href': member['topicRef']['href'].replace('#', ''),
                             'val': getBaseName(member['topicRef']['href'], gio)}
        return render_template('movies.html', data=data, asoc=association)

        return jsonify(association)
    else:
        abort(404)


@movies_bp.route('/association/<href>')
def association(href):
    gio = getTree()
    querie = gio.execute('$..topic[@.id is "%s"]' % href)
    data = list(querie)
    if len(data) == 1:
        data = data[0]
        querie = gio.execute('$..association["#%s" in @.member..href]' % href)
        association = list(querie)
        for ass in association:
            ass['instanceOf'] = getBaseName(ass['instanceOf']['topicRef']['href'], gio)
            member = list(filter(lambda x: x['topicRef']['href'] != ('#' + href), ass['member']))[0]
            ass['member'] = {'href': member['topicRef']['href'].replace('#', ''),
                             'val': getBaseName(member['topicRef']['href'], gio)}

        return render_template("association.html", data=data, asoc=association)
        return jsonify(association)
    else:
        abort(404)