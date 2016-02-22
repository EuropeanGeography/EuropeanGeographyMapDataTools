#!/usr/bin/python
import sys

from OSMParser import OMSParser
import jsonpickle


def main(file_name):
    parser = OMSParser(file_name)
    countries = parser.parse()
    for country in countries:
        print('processing ' + str(country))
        if country.iso2 is not None:
            output = open('output/' + country.iso2 + '.json', 'w')
            output.write(jsonpickle.encode(country))
            output.close()

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError:
        print('Usage: main.py file.osm')
