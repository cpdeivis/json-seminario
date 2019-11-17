# Seminário JSON
Seminário da disciplina de Linguagens de Marcação Extensível - ELC1092 de 2019/2.
Feito por: **Deivis Costa Pereira** e **William Felipe de Almeida Borges**.

## Pontos a serem abrangidos
* Transformar o [arquivo de filmes em XML](blob/master/files/GioMovies.xtm) para JSON, sem perder conteúdo;

* Validar o JSON criado com [JSON Schema](..blob/master/files/GioSchema.json) correspondente;

* [Aplicar consultas em JSON](..blob/master/queries.py):
    * Quais são os tipos de gênero de filmes, sem repetição?
    * Quais são os títulos dos filmes que foram produzidos em 2000, ordenados alfabeticamente?
    * Quais são os títulos em inglês dos filmes que tem a palavra “especial” na sinopse?
    * Quais são os sites dos filmes que são do tipo “thriller”?
    * Quantos filmes contém mais de 3 atores como elenco de apoio?
    * Quais são os ID dos filmes que tem o nome de algum membro do elenco citado na
sinopse?

* [Aplicar transformações em JSON](../blob/master/transform/):
    * Deve se construir um código que gere um conjunto de páginas HTML para cada nodo do grafo, onde nesta página possui a informação de cada tópico (seus nomes e ocorrências), além de links para todos os tópicos que estão associados com ele. A página inicial terá a apresentação do portal e o link para todos os filmes.

## Configurando
### Pré-requisitos

O projeto usa Python >=3.6.

### Instalando no Linux (Ubuntu)
Para instalar a versão correta do Python, adicione o PPA do [deadsnakes](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa)
```bash
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt-get install python3.6
```
Veja a versão do Python com o comando
```bash
python --version
```
Em seguida, instale o **pip**:
```bash
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.6 get-pip.py
```
E então, o **virtualenv**:
```bash
sudo pip3.6 install virtualenv
```
Clone o repositório:
```bash
git clone https://github.com/oscaruno/json-seminario
``` 
Crie o ambiente virtual dentro do diretório do repositório:
```bash
cd json-seminario
virtualenv venv -p python3.6
```
Ative o ambiente virtual com o seguinte comando: 
```bash
source venv/bin/activate
``` 
O nome do ambiente virtual deverá aparecer antes da CLI.

Instale os requisitos:
```bash
pip3.6 install -r requirements.txt
```
