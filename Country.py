class Country:

    iso2 = None
    name = None
    tags = {}
    polygons = None

    def __init__(self):
        pass

    def from_node(self, node):
        tag_nodes = node.findall('tag')
        for tag_node in tag_nodes:
            self.tags[tag_node.get('k')] = tag_node.get('v')
        self.name = self.tags['name']
        self.iso2 = self.tags['ISO3166-1:alpha2']
        return self.tags

    def assign_polygons(self, polygons):
        self.polygons = polygons
