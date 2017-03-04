import os
import sys
import time
import xml.etree.ElementTree as etree


def main(file_name):

    output_file = file_name + ".xapi" 
    time_stamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime())

    parser = etree.XMLParser(encoding='utf-8')
    tree = etree.parse(file_name, parser)

    for node in tree.findall('.//*[@id]'):
        node.attrib['version'] = '1'
        node.attrib['changeset'] = '1'
        node.attrib['timestamp'] = time_stamp

    tree.write(output_file, encoding='utf-8', method='xml')


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError:
print('Usage: xapi_attr.py file.osm')
