from enum import Enum

class _Element:
    def __init__(self, node):
        self.__parse_node(node)

    def __parse_node(self, node):
        pass

    def is_representing_country(self):
        return False


class ReferencingType(Enum):
    way = 'way'
    node = 'node'


class Relation(_Element):
    relation_id = None
    members = []
    tags = []

    def __parse_node(self, relation_tag):
        self.relation_id = relation_tag.get('id')
        for member_tag in relation_tag.findall('member'):
            self.members.append(Member(member_tag))
        for tag_tag in relation_tag.findall('tag'):
            self.members.append(Tag(tag_tag))

    def is_representing_country(self):
        return len(self.tags) > 0


class Member(_Element):
    ref = None
    type = None

    def __parse_node(self, member_tag):
        self.ref = int(member_tag.get('ref'))
        referencing_type = member_tag.get('type')
        if referencing_type == ReferencingType.way.value:
            self.type = ReferencingType.way
        elif referencing_type == ReferencingType.node.value:
            self.type = ReferencingType.node
        else:
            raise NameError('Unrecognized type: {0}!'.format(referencing_type))


class Tag(_Element):
    key = None
    value = None

    def __parse_node(self, tag_node):
        self.key = tag_node.get('k')
        self.value = tag_node.get('v')


class Node(_Element):
    node_id = None
    latitude = None
    longitude = None

    def __parse_node(self, node_tag):
        self.latitude = node_tag.get('lat')
        self.longitude = node_tag.get('lon')
        self.node_id = node_tag.get('id')


class Way(_Element):
    way_id = None
    tags = []
    nds = []

    def __parse_node(self, node):
        self.way_id = node.get('id')
        for element in node.findall('nd'):
            self.nds.append(Nd(element))
        for element in node.findall('tag'):
            self.tags.append(Tag(element))

    def is_representing_country(self):
        return len(self.tags) > 0


class Nd(_Element):
    ref = None

    def __parse_node(self, node):
        self.ref = node.get('ref')
