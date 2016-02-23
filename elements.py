from enum import Enum


class _Element:
    def __init__(self, node):
        self._parse_node(node)

    def _parse_node(self, node):
        pass

    def to_str(self):
        pass

    def is_representing_country(self):
        return False


class ReferencingType(Enum):
    way = 'way'
    node = 'node'


class Relation(_Element):

    def __init__(self, node):
        self.members = []
        self.tags = []
        super().__init__(node)

    def _parse_node(self, relation_tag):
        self.relation_id = relation_tag.get('id')
        for member_tag in relation_tag.findall('member'):
            self.members.append(Member(member_tag))
        for element in relation_tag.findall('tag'):
            self.tags.append(Tag(element))

    def is_representing_country(self):
        return len(self.tags) > 0

    def get_members(self):
        return self.members

    def get_tags(self):
        return self.get_tags()


class Member(_Element):

    def _parse_node(self, member_tag):
        self.ref = int(member_tag.get('ref'))
        referencing_type = member_tag.get('type')
        if referencing_type == ReferencingType.way.value:
            self.type = ReferencingType.way
        elif referencing_type == ReferencingType.node.value:
            self.type = ReferencingType.node
        else:
            raise NameError('Unrecognized type: {0}!'.format(referencing_type))


class Tag(_Element):

    def _parse_node(self, tag_node):
        self.key = tag_node.get('k')
        self.value = tag_node.get('v')


class Node(_Element):

    def _parse_node(self, node_tag):
        self.latitude = node_tag.get('lat')
        self.longitude = node_tag.get('lon')
        self.node_id = node_tag.get('id')

    def to_dict(self):
        return {'lat': self.latitude, 'lon': self.longitude}

    def to_str(self):
        return str({'id': self.node_id, 'lat': self.latitude, 'lon': self.longitude})


class Way(_Element):

    def __init__(self, node):
        self.tags = []
        self.nds = []
        super().__init__(node)

    def _parse_node(self, node):
        self.way_id = node.get('id')
        for element in node.findall('nd'):
            self.nds.append(Nd(element))
        for element in node.findall('tag'):
            self.tags.append(Tag(element))

    def is_representing_country(self):
        return len(self.tags) > 0

    def to_str(self):
        return {'id': self.way_id, 'tag_count': len(self.tags)}


class Nd(_Element):
    ref = None

    def _parse_node(self, node):
        self.ref = node.get('ref')
