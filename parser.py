import os

import elements
import xml.etree.ElementTree as ElementTree

from Country import Country


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
                print("Found element '{0}'!".format(element))
                relation = elements.Relation(element)
                self.relations[relation.relation_id] = relation
            elif element.tag == 'node':
                node = elements.Node(element)
                self.nodes[node.node_id] = node
            elif element.tag == 'way':
                way = elements.Way(element)
                self.ways[way.way_id] = way
                print('Found way {0}'.format(way.to_str()))

    def __extract_country(self, source, source_type):
        if source.is_representing_country():
            # print('extracting {0} with id={1} and tags={2}'.format(str(source), source.way_id, source.tags[1].value))
            if source_type == 'way':
                nodes = []
                tags = {}
                for nd in source.nds:
                    nodes.append(self.nodes[nd.ref].to_dict())
                for tag in source.tags:
                    tags[tag.key] = tag.value
                print('obtained tags ' + str(tags))
                return Country(polygons=[nodes], tags=tags)
            elif source_type == 'relation':
                return self.__extract_from_relation(source)
        raise ValueError('Source {0} is not representing country!'.format(source))

    def __extract_from_relation(self, source):
        print('extracting {0} relation'.format(source))
        nodes = []
        ways = []
        tags = {}
        polygons = []
        for member in source.members:
            if member.type == elements.ReferencingType.node:
                nodes.append(self.nodes[member.ref].to_dict())
            elif member.type == elements.ReferencingType.way:
                referenced_way = self.ways[str(member.ref)]
                nodes_of_referenced_way = []
                ways.append(referenced_way)
                for nd in referenced_way.nds:
                    nodes_of_referenced_way.append(self.nodes[nd.ref].to_dict())
                polygons.append(nodes_of_referenced_way)
        for tag in source.tags:
            tags[tag.key] = tag.value
        print('extracted {0} relation'.format(source))
        return Country(polygons=polygons, tags=tags)

    def __write_country_to_file(self, source, source_type):
        path = 'output/'
        country = self.__extract_country(source, source_type)
        if not os.path.exists(path):
            os.mkdir(path)
        output = open(path + country.iso2 + '.json', 'w')
        output.write(country.to_json())
        output.close()
        print('wrote {0} country with tags {1}'.format(country.name, country.tags))

    def __process_tags(self):
        for relation in self.relations.values():
            print('processing {0} relation'.format(relation))
            if relation.is_representing_country():
                print('Representing country {0} relation'.format(relation))
                self.__write_country_to_file(source=relation, source_type='relation')
        for way in self.ways.values():
            if way.is_representing_country():
                print('processing {0} with id={1} and tags={2}'.format(str(way), way.way_id, way.tags[1].value))
                self.__write_country_to_file(source=way, source_type='way')
