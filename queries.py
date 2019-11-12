import json
from objectpath import Tree


def main():
    with open("files/GioMovies.json", "r") as file:
        data = json.load(file)
    giomovies = Tree(data)

    # Quais são os tipos de gênero de filmes, sem repetição?
    q1 = giomovies.execute('$..topic[@.instanceOf.topicRef.href is "#Genero"].id')
    print("1: Gêneros: %s\n" % list(q1))

    # Quais são os títulos dos filmes que foram produzidos em 2000, ordenados alfabeticamente?
    q2 = giomovies.execute("sort($..topic[@.id in array($..association['#id_2000' in @.member..href]"
                           ".member[@[0]]..href[replace(@, '#', '')])]..baseNameString)")
    print("2: Filmes 2000: %s\n" % list(q2))

    # Quais são os títulos em inglês dos filmes que tem a palavra “especial” na sinopse?
    q3 = giomovies.execute("$..topic[count(@..occurrence['#sinopse' in @..href].resourceData['especial' in @]) > "
                           "0]..occurrence['#ingles' in @..href].resourceData")
    print("3: Filmes 'Especial': %s\n" % list(q3))

    # Quais são os sites dos filmes que são do tipo “thriller”?
    q4 = giomovies.execute("$..topic[@.id in array($..association['#thriller' in @.member..href]"
                           ".member[@[0]]..href[replace(@, '#', '')])]"
                           "..occurrence['#site' in @..href]..resourceRef.href")
    print("4: Filmes Thriller: %s\n" % list(q4))

    # Quantos filmes contém mais de 3 atores como elenco de apoio?
    q5 = giomovies.execute("$..topic[count(@..occurrence['#elencoApoio' in @..href])>3]..baseNameString")
    print("5: 3+ Elenco Apoio: %s\n" % list(q5))

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
    for x in list(filter(lambda y: 'occurrence' in y and bsino(y['occurrence']), data['topicMap']['topic'])):
        if any(ator in sino(x['occurrence']) for ator in apoio(x['occurrence'])) or any(
                ator in sino(x['occurrence']) for ator in elenco(x['id'])):
            q6.append(_name(x['id']))
    print("6: Sinopse com autor: %s" % q6)


if __name__ == '__main__':
    main()
