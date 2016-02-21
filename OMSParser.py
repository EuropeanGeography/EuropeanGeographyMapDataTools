from Node import Node

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
    nodes = {}

    parser = ET.XMLParser(encoding='utf-8')
    tree = None
    root = None

    def __init__(self, file_name):
        self.tree = ET.parse(file_name, self.parser)
        self.root = self.tree.getroot()

    def get_node(self, node_id):
        """
        Tries to obtain the node from cache, if it is not a hit, walk through document will be performed
        :param node_id: id of node which are being found
        :return: found node or throws an exception if node is not found
        """
        if node_id in self.nodes:  # cache hit
            return self.nodes[node_id]
        return self.find_node(node_id)

    def is_node_in_cache(self, node_id):
        return node_id in self.nodes

    def find_node(self, node_id):
        """
        Will walk through all node tags in parsed document
        :param node_id: id of node which are being found
        :return: found node or throws an exception if node is not found
        """
        for tag in self.root.findall('node'):
            node = self.translate_node_tag_to_object(tag)
            if not self.is_node_in_cache(node.id):
                self.nodes[node.id] = node
            if node.id == node_id:
                return node
        raise NameError('Node tag with id ' + str(node_id) + ' not found!')

    @staticmethod
    def translate_node_tag_to_object(node_tag):
        node_id = int(node_tag.get('id'))
        latitude = float(node_tag.get('lat'))
        longitude = float(node_tag.get('lon'))
        return Node(node_id, latitude, longitude)
