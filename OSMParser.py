from Country import Country
from Node import Node
from Polygon import Polygon
from PolygonGroup import PolygonGroup

try:
    from lxml import ET

    print("running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as ET

        print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as ET

            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as ET

                print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as ET

                    print("running with ElementTree")
                except ImportError:
                    print("Failed to import ElementTree from any known place")


class OMSParser:
    __nodes = {}
    __ways = {}
    countries = []

    __parser = ET.XMLParser(encoding='utf-8')
    __tree = None
    __root = None

    def __init__(self, file_name):
        self.__tree = ET.parse(file_name, self.__parser)
        self.__root = self.__tree.getroot()

    def get_node(self, node_id):
        """
        Tries to obtain the node from cache, if it is not a hit, walk through document will be performed
        :param node_id: id of node which are being found
        :return: found node or throws an exception if node is not found
        """
        if node_id in self.__nodes:  # cache hit
            return self.__nodes[node_id]
        return self.find_node(node_id)

    def is_node_in_cache(self, node_id):
        return node_id in self.__nodes

    def is_way_in_cache(self, way_id):
        return way_id in self.__ways

    def get_way_tag(self, way_id):
        if self.is_way_in_cache(way_id):
            return self.__ways[way_id]
        return self.find_way_tag(way_id)

    def find_node(self, node_id):
        """
        Will walk through all node tags in parsed document
        :param node_id: id of node which are being found
        :return: found node or throws an exception if node is not found
        """
        for tag in self.__root.findall('node'):
            node = self.translate_node_tag_to_object(tag)
            if not self.is_node_in_cache(node.id):
                self.__nodes[node.id] = node
            if node.id == node_id:
                return node
        raise NameError('Node tag with id ' + str(node_id) + ' not found!')

    def find_way_tag(self, way_id):
        for tag in self.__root.findall('way'):
            node_id = tag.get('id')
            if not self.is_way_in_cache(node_id):
                self.__ways[node_id] = tag
            if int(node_id) == int(way_id):
                return tag
        raise NameError('Way tag with id ' + str(way_id) + ' not found!')

    @staticmethod
    def translate_node_tag_to_object(node_tag):
        node_id = int(node_tag.get('id'))
        latitude = float(node_tag.get('lat'))
        longitude = float(node_tag.get('lon'))
        return Node(node_id, latitude, longitude)

    def parse_relation(self, relation_node):
        """
        Parses relation, which is object which usually represents e.g. country. It consists of multiple ways and nodes.
        Ways then contains links to nodes too.
        :param relation_node: whole relation node which contains all ways and node links
        :return: Country object containing all tags from relation and polygons (parsed ways).
        """
        polygons = PolygonGroup()  # todo missing bounding box
        for referencing in relation_node.findall('member'):
            node_type = referencing.get('type')
            if node_type == 'way':
                polygons.add_polygon(self.parse_way_node(self.get_way_tag(referencing.get('ref')), 'nd'))
            if node_type == 'node':
                raise ValueError('This value is not expected!')

        country = Country()
        country.from_node(relation_node)  # extracts tag nodes
        country.assign_polygons(polygons)
        return country

    def parse_way_node(self, way_node, referencing_type='member'):
        """
        Creates polygon containing all nodes referenced by given way node
        :param referencing_type: Name of tag which is referencing to <code>node</code> tag
        :param way_node: node which will be parsed
        :return: polygon object
        """
        polygon = Polygon()
        for node_reference_tag in way_node.findall(referencing_type):
            node_id = node_reference_tag.get('ref')
            polygon.add_point(self.get_node(node_id))
        return polygon

    def create_country_from_way(self, way_node):
        polygon = self.parse_way_node(way_node)
        country = Country()
        country.from_node(way_node)  # extracts tag nodes
        country.assign_polygons([polygon])
        return country

    def create_country_from_relation(self, relation_node):
        return self.parse_relation(relation_node)

    def parse(self):
        for node in self.__root.findall('relation'):
            self.countries.append(self.create_country_from_relation(node))
        for node in self.__root.findall('way'):
            if not self.is_way_in_cache(node.get('id')):
                self.countries.append(self.create_country_from_way(node))
        return self.countries
