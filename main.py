import sys

from OSMParser import OMSParser
import jsonpickle


def main(file_name):
    parser = OMSParser(file_name)
    countries = parser.parse()
    output = open(file_name + '.json', 'w')
    output.write(jsonpickle.encode(countries))
    output.close()

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError:
        print('Usage: main.py file.osm')
