import os
import json
from lxml import etree
from jsonschema import validate


def convert(tree):
    """ Converte de forma genérica qq XML para JSON
    :param tree: Arquivo XML em lxml.etree
    :return: JSON
    """
    XSL = etree.XSLT(etree.parse('files/xml2json.xsl'))
    json_text = XSL(tree)
    data = json.loads(str(json_text))
    return data


def main():
    # Carrega o arquivo original para uma representação da lib 'lxml'
    gioxtm = etree.parse("files/GioMovies.xtm")
    data = convert(gioxtm)
    # Carrega o JSONSchema
    with open("files/GioSchema.json", "r") as file:
        schema = json.load(file)

    try:
        # tenta validar o JSON gerado com seu respectivo Schema
        validate(instance=data, schema=schema)
        # Caso a validação tenha sucesso, grava a informação no arquivo de saída
        if os.path.exists("files/GioMovies.json"):
            os.remove("files/GioMovies.json")  # remove se o arquivo já existe
        with open("files/GioMovies.json", "w") as file:
            json.dump(data, file)
    except:
        print("A Validação deu Errado!!!")


if __name__ == '__main__':
    main()
