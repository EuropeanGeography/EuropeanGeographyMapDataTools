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
                relation = elements.Relation(element)
                self.relations[relation.relation_id] = relation
            elif element.tag == 'node':
                node = elements.Node(element)
                self.nodes[node.node_id] = node
            elif element.tag == 'way':
                way = elements.Way(element)
                self.ways[way.way_id] = way

    def __extract_country(self, source, source_type):
        if source_type == 'way':
            nodes = []
            tags = {}
            for nd in source.nds:
                nodes.append(self.nodes[nd.ref])
            for tag in source.tags:
                tags[tag.key] = tag.value
            return Country(polygons=[nodes], tags=source.tags)
        elif source_type == 'relation':
            return self.__extract_from_relation(source)


    def __extract_from_relation(self, source):


    def __write_country_to_file(self, source, source_type):
        country = self.__extract_country(source, source_type)
        output = open('output/' + country.iso2 + '.json', 'w')
        output.write(country.to_JSON())
        output.close()

    def __process_tags(self):
        for relation in self.relations:
            if relation.is_representing_country():
                self.__write_country_to_file(source=relation, source_type='relation')
        for way in self.ways:
            if way.is_representing_country():
                self.__write_country_to_file(source=way, source_type='way')
