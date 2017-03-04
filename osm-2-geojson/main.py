#!/usr/bin/python3
import sys
import parser


def main(file_name):
    parser.Parser(file_name)


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError:
        print('Usage: main.py file.osm')
