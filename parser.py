import os

import elements
import hooks
import xml.etree.ElementTree as ElementTree

from country import Country


class Parser:
    __parser = ElementTree.XMLParser(encoding='utf-8')
    __tree = None
    __root = None

    relations = {}
    ways = {}
    nodes = {}

    def __init__(self, file_name):
        self.__tree = ElementTree.parse(file_name, self.__parser)
        self.__root = self.__tree.getroot()
        self.__load_to_memory()
        self.__process_tags()

    def __load_to_memory(self):
        for element in self.__root.iter():
            if element.tag == 'relation':
                relation = elements.Relation(element)
                self.relations[relation.relation_id] = relation
            elif element.tag == 'node':
                node = elements.Node(element)
                self.nodes[node.node_id] = node
            elif element.tag == 'way':
                way = elements.Way(element)
                self.ways[way.way_id] = way

    def __extract_country(self, source, source_type):
        if source.is_representing_country():
            if source_type == 'way':
                return Country.extract_from_way(source=source, nodes=self.nodes)
            elif source_type == 'relation':
                return Country.extract_from_relation(source=source, nodes=self.nodes, ways=self.ways)
        raise ValueError('Source {0} is not representing country!'.format(source))

    def __process_source(self, source, source_type):
        country = self.__extract_country(source, source_type)
        self.__write_country_to_file(country=country)
        hooks.process_country(country=country)

    def __write_country_to_file(self, country):
        path = 'output/'
        if not os.path.exists(path):
            os.mkdir(path)
        output = open(path + country.iso2.lower() + '.json', 'w')
        output.write(country.to_json())
        output.close()

        geojsonpath = 'data/'
        if not os.path.exists(geojsonpath):
            os.mkdir(geojsonpath)
        output = open(geojsonpath + country.iso2.lower() + '.geo.json', 'w')
        output.write(country.to_geojson())
        output.close()


    def __process_tags(self):
        for relation in self.relations.values():
            if relation.is_representing_country():
                self.__process_source(source=relation, source_type='relation')
        for way in self.ways.values():
            if way.is_representing_country():
                self.__process_source(source=way, source_type='way')
