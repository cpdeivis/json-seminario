import os
import json
from lxml import etree
from jsonschema import validate


def convert(tree):
    XSL = etree.XSLT(etree.parse('files/xml2json.xsl'))
    json_text = XSL(tree)
    data = json.loads(str(json_text))
    return data


def main():
    gioxtm = etree.parse("files/GioMovies.xtm")
    data = convert(gioxtm)
    with open("files/GioSchema.json", "r") as file:
        schema = json.load(file)

    try:
        validate(instance=data, schema=schema)
        if os.path.exists("files/GioMovies.json"):
            os.remove("files/GioMovies.json")

        with open("files/GioMovies.json", "w") as file:
            json.dump(data, file)
    except:
        print("Algo deu errado")


if __name__ == '__main__':
    main()
