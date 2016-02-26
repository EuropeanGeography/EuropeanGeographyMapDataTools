import json
import copy

import elements

try:
    from country_bounding_boxes import (
        country_subunits_containing_point,
        country_subunits_by_iso_code
    )
except ImportError:  # ignore
    print("Error importing country_bounding_boxes, is this package installed?")


class Country:
    name = None
    iso2 = None
    tags = {}
    polygons = []

    def __init__(self, polygons, tags):
        self.polygons = polygons
        self.tags = tags
        self.name = self.tags['name']
        self.iso2 = self.tags['ISO3166-1:alpha2']

    def assign_polygons(self, polygons):
        self.polygons = polygons

    def to_json(self):
        wrapper = copy.deepcopy(self.tags)
        wrapper['bounding-boxes'] = [c.bbox for c in country_subunits_by_iso_code(self.iso2)]
        wrapper['polygons'] = self.polygons
        return json.dumps(wrapper)

    @staticmethod
    def extract_from_relation(source, nodes, ways):
        """
        Extracts instance of Country from instance of Relation

        :param source: source instance of Relation, from which the Country instance will be extracted
        :param nodes: list of Node instances, containing all parsed nodes from document from which the source comes
        :param ways: list of Way instances, containing all parsed ways from document from which the source comes
        :return: instance of country containing all necessary information
        """
        referenced_nodes = []
        tags = {}
        polygons = []
        for member in source.members:
            # type of referenced element is node
            if member.type == elements.ReferencedType.node:
                referenced_nodes.append(nodes[member.ref].to_dict())
            # type of referenced element is way
            elif member.type == elements.ReferencedType.way:
                referenced_way = ways[str(member.ref)]
                nodes_of_referenced_way = []
                for nd in referenced_way.nds:  # nd is element referencing to nodes
                    # extracting nodes referenced by way referenced by relation
                    nodes_of_referenced_way.append(nodes[nd.ref].to_dict())
                polygons.append(nodes_of_referenced_way)
        for tag in source.tags:
            tags[tag.key] = tag.value
        return Country(polygons=polygons, tags=tags)

    @staticmethod
    def extract_from_way(source, nodes):
        """
        Extracts instance of Country from instance of Way

        :param source: source instance of Way, from which the Country instance will be extracted
        :param nodes: list of Node instances, containing all parsed nodes from document from which the source comes
        :return: instance of country containing all necessary information
        """
        referenced_nodes = []
        tags = {}
        # nd is element referencing to nodes
        for nd in source.nds:
            referenced_nodes.append(nodes[nd.ref].to_dict())
        for tag in source.tags:
            tags[tag.key] = tag.value
        return Country(polygons=[referenced_nodes], tags=tags)
