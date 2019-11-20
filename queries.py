import json
import time
import re
from objectpath import Tree


def main():
    with open("files/GioMovies.json", "r") as file:
        data = json.load(file)
    giomovies = Tree(data)

    # Quais são os tipos de gênero de filmes, sem repetição?
    clock = time.time()
    q1 = giomovies.execute('$..topic[@.instanceOf.topicRef.href is "#Genero"].id')
    print("1: Gêneros: %s" % list(q1))
    print("em ", time.time() - clock, " segundos\n")

    # Quais são os títulos dos filmes que foram produzidos em 2000, ordenados alfabeticamente?
    clock = time.time()
    q2 = giomovies.execute("sort($..topic[@.id in array($..association['#id_2000' in @.member..href]"
                           ".member[@[0]]..href[replace(@, '#', '')])]..baseNameString)")
    print("2: Filmes 2000: %s" % list(q2))
    print("em ", time.time() - clock, " segundos\n")

    # Quais são os títulos em inglês dos filmes que tem a palavra “especial” na sinopse?
    clock = time.time()
    q3 = giomovies.execute("$..topic[count(@..occurrence['#sinopse' in @..href].resourceData['especial' in @]) > "
                           "0]..occurrence['#ingles' in @..href].resourceData")
    print("3: Filmes 'Especial': %s" % list(q3))
    print("em ", time.time() - clock, " segundos\n")

    # Quais são os sites dos filmes que são do tipo “thriller”?
    clock = time.time()
    q4 = giomovies.execute("$..topic[@.id in array($..association['#thriller' in @.member..href]"
                           ".member[@[0]]..href[replace(@, '#', '')])]"
                           "..occurrence['#site' in @..href]..resourceRef.href")
    print("4: Filmes Thriller: %s" % list(q4))
    print("em ", time.time() - clock, " segundos\n")

    # Quantos filmes contém mais de 3 atores como elenco de apoio?
    clock = time.time()
    q5 = giomovies.execute("$..topic[count(@..occurrence['#elencoApoio' in @..href])>3]..baseNameString")
    print("5: 3+ Elenco Apoio: %s" % len(list(q5)))
    print("em ", time.time() - clock, " segundos\n")

    # Quais são os ID dos filmes que tem o nome de algum membro do elenco citado na sinopse
    # Pega a Sinopse
    sino = lambda ls: \
        list(map(lambda x: x['resourceData'], list(filter(lambda oc: ('scope' in oc and 'topicRef' in oc['scope'] and
                                                                      oc['scope']['topicRef']['href'] == '#sinopse'),
                                                          ls))))[0]
    bsino = lambda ls: type(ls) == list and len(list(filter(lambda oc: 'scope' in oc and 'topicRef' in oc['scope'] and
                                                                       oc['scope']['topicRef']['href'] == '#sinopse',
                                                            ls))) > 0
    # Pega Elenco Apoio
    apoio = lambda ls: list(map(lambda x: x['resourceData'], list(
        filter(lambda oc: ('scope' in oc and 'topicRef' in oc['scope']
                           and oc['scope']['topicRef']['href'] == '#elencoApoio'), ls))))
    # Pega elenco
    _elenco = lambda x, id: next(iter(list(map(lambda el: el['topicRef']['href'], list(
        filter(lambda el: el['topicRef']['href'].replace('#', '') != id, x))))), '')
    _name = lambda x: list(filter(lambda top: top['id'] == x, data['topicMap']['topic']))[0]['baseName'][
        'baseNameString']
    elenco = lambda id: list(map(lambda el: _name(_elenco(el['member'], id).replace('#', '')),
                                 list(filter(lambda mb: mb['instanceOf']['topicRef']['href'] == '#filme-elenco' and
                                                        any(memb['topicRef']['href'].replace('#', '') == id for memb in
                                                            mb['member']), data['topicMap']['association']))))
    q6 = []
    clock = time.time()
    for x in list(filter(lambda y: 'occurrence' in y and bsino(y['occurrence']), data['topicMap']['topic'])):
        if any(ator in sino(x['occurrence']) for ator in apoio(x['occurrence'])) or any(
                ator in sino(x['occurrence']) for ator in elenco(x['id'])):
            q6.append(x['id'])
    print("6: Sinopse com ator: %s" % q6)
    print("em ", time.time() - clock, " segundos\n")

    q3 = []

    benglish = lambda ls: type(ls) == list and len(list(filter(lambda oc: 'scope' in oc and 'topicRef' in oc['scope'] and
                                                                       oc['scope']['topicRef']['href'] == '#ingles',
                                                            ls))) > 0
    english = lambda ls: \
        list(map(lambda x: x['resourceData'], list(filter(lambda oc: ('scope' in oc and 'topicRef' in oc['scope'] and
                                                                      oc['scope']['topicRef']['href'] == '#ingles'),
                                                          ls))))[0]
    clock = time.time()
    for x in list(filter(lambda y: 'occurrence' in y and bsino(y['occurrence']), data['topicMap']['topic'])):
        if re.search(r'\b(especial)\b', sino(x['occurrence'])) and benglish(x['occurrence']):
            q3.append(english(x['occurrence']))
    print("3: Sinopse com 'especial': %s" % q3)
    print("em ", time.time() - clock, " segundos\n")



if __name__ == '__main__':
    main()
