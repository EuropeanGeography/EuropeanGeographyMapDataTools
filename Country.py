import json
import copy

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
