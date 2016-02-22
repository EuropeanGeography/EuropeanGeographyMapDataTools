#!/usr/bin/python
import sys

from OSMParser import OMSParser
import jsonpickle


def main(file_name):
    parser = OMSParser(file_name)
    countries = parser.parse()
    for country in countries:
        output = open(country.iso2 + '.json', 'w')
        output.write(jsonpickle.encode(country))
        output.close()

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError:
        print('Usage: main.py file.osm')
