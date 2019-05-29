import xml.etree.ElementTree as ET

from opencmiss.utils.zinc import AbstractNodeDataObject


class MBFXMLException(Exception):
    pass


class MBFPoint(AbstractNodeDataObject):

    def __init__(self, x, y, z, diameter=0.0):
        super(MBFPoint, self).__init__(['coordinates', 'radius'])
        self._x = x
        self._y = y
        self._z = z
        self._radius = diameter / 2.0

    def get(self):
        return [self._x, self._y, self._z, self._radius]

    def coordinates(self):
        return [self._x, self._y, self._z]

    def radius(self):
        return self._radius

    def scale(self, scale):
        self._x = self._x * scale[0]
        self._y = self._y * scale[1]

    def offset(self, offset):
        self._x = self._x + offset[0]
        self._y = self._y + offset[1]
        self._z = self._z + offset[2]

    def __repr__(self):
        return 'x="{0}" y="{1}" z="{2}" r="{3}"'.format(self._x, self._y, self._z, self._radius)


def convert_hex_to_rgb(hex_string):
    hex_string = hex_string.lstrip('#')
    return [int(hex_string[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]


def get_raw_tag(element):
    element_tag = element.tag
    if '}' in element_tag:
        element_tag = element.tag.split('}', 1)[1]
    return element_tag


def parse_contour(contour_root):
    contour = {'colour': contour_root.attrib['color'],
               'rgb': convert_hex_to_rgb(contour_root.attrib['color']),
               'closed': contour_root.attrib['closed'] == 'true',
               'name': contour_root.attrib['name']}
    data = []
    for child in contour_root:
        raw_tag = get_raw_tag(child)
        if raw_tag == "point":
            data.append(MBFPoint(float(child.attrib['x']),
                                 float(child.attrib['y']),
                                 float(child.attrib['z']),
                                 float(child.attrib['d'])))
        elif raw_tag == "property":
            pass
        elif raw_tag == "resolution":
            pass
        else:
            raise MBFXMLException("XML format violation unknown tag {0}".format(raw_tag))
    contour['data'] = data
    return contour


def main(filename):
    root = ET.parse(filename).getroot()
    data = []
    for child in root:
        raw_tag = get_raw_tag(child)
        if raw_tag == "contour":
            contour_data = parse_contour(child)
            data.append(contour_data)

    coordinates = []
    for points in data:
        for p in points['data']:
            coordinates.append(p.coordinates())

    return coordinates


if __name__ == '__main__':
    main('test.xml')
