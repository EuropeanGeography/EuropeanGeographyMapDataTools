import json


class PolygonGroup:
    bounding_boxes = None
    polygons = []

    def __init__(self):
        pass

    def add_polygon(self, polygon):
        self.polygons.append(polygon)

    def get_polygons(self):
        return self.polygons

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
        # wrapper_list = []
        # for polygon in self.polygons:
        #    wrapper_list.append(polygon.get_wrapper_dict())
        # wrapper_dict = {self.bounding_box: wrapper_list}
        # return json.dumps(wrapper_dict)
