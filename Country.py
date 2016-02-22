import json


class Country:
    tag_dict = {}
    polygons = None

    def __init__(self):
        pass

    def from_node(self, node):
        tag_nodes = node.findall('tag')
        for tag_node in tag_nodes:
            self.tag_dict[tag_node.get('k')] = tag_node.get('v')

        return self.tag_dict

    def assign_polygons(self, polygons):
        self.polygons = polygons
