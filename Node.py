class Node:

    id = -999999999
    latitude = -999
    longitude = -999

    def __init__(self, node_id, latitude, longitude):
        assert node_id is not None
        assert latitude is not None
        assert longitude is not None
        self.id = node_id
        self.latitude = latitude
        self.longitude = longitude



