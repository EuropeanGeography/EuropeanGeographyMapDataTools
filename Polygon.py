import json


class Polygon:

    points = []

    def __init__(self):
        pass

    def add_point(self, point):
        self.points.append(point)

    def get_wrapper_dict(self):
        return {'polygon': self.points}

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
        # return json.dumps(self.get_wrapper_dict())
