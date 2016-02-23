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
