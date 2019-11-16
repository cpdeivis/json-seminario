from flask import Blueprint, render_template, jsonify, abort
import json
from objectpath import Tree

movies_bp = Blueprint('movies', __name__)


def getTree():
    """ Retorna a Tree(objectpath) do arquivo GioMovies
        Utilizada para todas as queries/pesquisas
    """
    with open('../files/GioMovies.json', 'r') as file:
        data = json.load(file)
    file.close()
    return Tree(data)


def getBaseName(id, tree):
    """ Executa uma busca no Tree e retorna o nome do tópico
        :param: id: Identificação do tópico com o #
        :param: tree: getTree()
    """
    querie = tree.execute('$..topic[@.id is "%s"]' % id.replace('#', ''))
    data = list(querie)[0]
    try:
        # Handle do baseName list ou dict
        if type(data['baseName']) is list:
            return data['baseName'][0]['baseNameString']
        return data['baseName']['baseNameString']
    except:
        return ''


@movies_bp.route('/')
@movies_bp.route('/index')
def index():
    """ View padrão, retorna uma lista de todos os filmes
    """
    gio = getTree()
    # Busca na Tree todos os tópicos do tipo filme
    querie = gio.execute('$..topic[@.instanceOf.topicRef.href is "#Filme"]')
    data = list(querie)
    return render_template("index.html", data=data)


def occurrence(ocr, gio):
    """ Remapeia uma entrada do tipo occurrence
        :param ocr: ['occurrence']
        :param gio: getTree()
    """
    # Trata basicamente o caso ocr['scope']['topicRef']['href'] = '#site'
    if 'scope' in ocr:
        ocr['scope'] = getBaseName(ocr['scope']['topicRef']['href'], gio)
    elif 'instanceOf' in ocr:
        ocr['scope'] = getBaseName(ocr['instanceOf']['topicRef']['href'], gio)
        ocr['resourceData'] = ocr['resourceRef']['href']
        del ocr['instanceOf']
        del ocr['resourceRef']


@movies_bp.route('/movies/<id>')
def movies(id):
    """ View de Filme
    :param id: Identificador do Filme, sem #
    :return: informações do filme com associações
    """
    gio = getTree()
    # Busca o tópico do parametro informado
    querie = gio.execute('$..topic[@.id is "%s" and @.instanceOf.topicRef.href is "#Filme"]' % id)
    data = list(querie)
    # Verifica se o filme existe senão 404
    if len(data) == 1:
        data = data[0]
        # Adapta todas as 'occurrence' para o Jinja2
        if type(data['occurrence']) is list:
            for ocr in data['occurrence']:
                occurrence(ocr, gio)
        else:
            # Trata o caso de ter somente uma 'occurrence'
            occurrence(data['occurrence'], gio)
            data['occurrence'] = [data['occurrence']]

        # Busca todas as 'association' deste Filme
        querie = gio.execute('$..association["#%s" in @.member..href]' % id)
        association = list(querie)
        # Adapta as 'association' para o Jinja2
        for ass in association:
            ass['instanceOf'] = getBaseName(ass['instanceOf']['topicRef']['href'], gio)
            member = list(filter(lambda x: x['topicRef']['href'] != ('#' + id), ass['member']))[0]
            ass['member'] = {'href': member['topicRef']['href'].replace('#', ''),
                             'val': getBaseName(member['topicRef']['href'], gio)}
        return render_template('movies.html', data=data, asoc=association)

        # return jsonify(association)
    else:
        abort(404)


@movies_bp.route('/association/<href>')
def association(href):
    """ O que está Associado com um tópico
    :param href: Identificação do tópico sem #
    :return: A lista de filmes associados com este Tópico
    """
    gio = getTree()
    querie = gio.execute('$..topic[@.id is "%s"]' % href)
    data = list(querie)
    # Handle da existência do tópico senão 404
    if len(data) == 1:
        data = data[0]
        # Realiza a busca do que está associado com o tópico
        querie = gio.execute('$..association["#%s" in @.member..href]' % href)
        association = list(querie)
        for ass in association:
            # Adapta para o Jinja2
            ass['instanceOf'] = getBaseName(ass['instanceOf']['topicRef']['href'], gio)
            member = list(filter(lambda x: x['topicRef']['href'] != ('#' + href), ass['member']))[0]
            ass['member'] = {'href': member['topicRef']['href'].replace('#', ''),
                             'val': getBaseName(member['topicRef']['href'], gio)}

        return render_template("association.html", data=data, asoc=association)
        # return jsonify(association)
    else:
        abort(404)
