import json
from objectpath import Tree


def main():
    with open("GioMovies.json", "r") as file:
        data = json.load(file)
    giomovies = Tree(data)

    # Quais são os tipos de gênero de filmes, sem repetição?
    q1 = giomovies.execute('$..topic[@.instanceOf.topicRef.href is "#Genero"].id')

    # Quais são os títulos dos filmes que foram produzidos em 2000, ordenados alfabeticamente?
    q2 = giomovies.execute("sort($..topic[@.id in array($..association['#id_2000' in @.member..href]"
                           ".member[@[0]]..href[replace(@, '#', '')])]..baseNameString)")

    # Quais são os títulos em inglês dos filmes que tem a palavra “especial” na sinopse?
    q3 = giomovies.execute("$..topic[count(@..occurrence['#sinopse' in @..href].resourceData['especial' in @]) > "
                           "0]..occurrence['#ingles' in @..href].resourceData")

    # Quais são os sites dos filmes que são do tipo “thriller”?
    q4 = giomovies.execute("$..topic[@.id in array($..association['#thriller' in @.member..href]"
                           ".member[@[0]]..href[replace(@, '#', '')])]"
                           "..occurrence['#site' in @..href]..resourceRef.href")

    # Quantos filmes contém mais de 3 atores como elenco de apoio?
    q5 = giomovies.execute("$..topic[count(@..occurrence['#elencoApoio' in @..href])>3]..baseNameString")

    # Quais são os ID dos filmes que tem o nome de algum membro do elenco citado na sinopse
    # TODO: NÃO ESTÁ FUNCIONANDO AINDA
    q6 = giomovies.execute("$..topic["
                           "@..occurrence['#sinopse' in @..href].resourceData["
                           "@..occurrence['#elencoApoio' in @..href].resourceData in @]"
                           "].id")

if __name__ == '__main__':
    main()
