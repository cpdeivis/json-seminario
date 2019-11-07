# Seminário JSON
Seminário da disciplina de Linguagens de Marcação Extensível - ELC1092 de 2019/2.
Feito por: **Deivis Costa Pereira** e **William Felipe de Almeida Borges**.

## Pontos a serem abrangidos
* Transformar o [arquivo de filmes em XML](..blob/master/files/GioMovies.xtm) para JSON, sem perder conteúdo;

* Validar o JSON criado com [JSON Schema](..blob/master/files/GioSchema.json) correspondente;

* Aplicar consultas em JSON:
    * Quais são os tipos de gênero de filmes, sem repetição?
    * Quais são os títulos dos filmes que foram produzidos em 2000, ordenados alfabeticamente?
    * Quais são os títulos em inglês dos filmes que tem a palavra “especial” na sinopse?
    * Quais são os sites dos filmes que são do tipo “thriller”?
    * Quantos filmes contém mais de 3 atores como elenco de apoio?
    * Quais são os ID dos filmes que tem o nome de algum membro do elenco citado na
sinopse?

* Aplicar transformações em JSON:
    * Deve se construir um código que gere um conjunto de páginas HTML para cada nodo do grafo, onde nesta página possui a informação de cada tópico (seus nomes e ocorrências), além de links para todos os tópicos que estão associados com ele. A página inicial terá a apresentação do portal e o link para todos os filmes.