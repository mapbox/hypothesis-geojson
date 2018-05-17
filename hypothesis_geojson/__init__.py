# encoding: utf-8
"""
A hypothesis strategy for generating GeoJSON
"""
__version__ = '0.1'


from hypothesis.strategies import (
    assume, booleans, composite, dictionaries, floats, integers, lists, none,
    one_of, sampled_from, text, tuples)


@composite
def positions(draw, dims=2):
    """
    https://tools.ietf.org/html/rfc7946#section-3.1.1

    Questions
    ---------
    * should the elevation/altitude component be bounded?
    * is it valid to mix dimensionality of positions within a geometry?
    """
    if dims is None:
        dims = draw(sampled_from([2, 3]))

    if dims == 2:
        pos = draw(
            tuples(
                floats(min_value=-180, max_value=180, allow_nan=False, allow_infinity=False),
                floats(min_value=-90, max_value=90, allow_nan=False, allow_infinity=False)))
    elif dims == 3:
        pos = draw(
            tuples(
                floats(min_value=-180, max_value=180, allow_nan=False, allow_infinity=False),
                floats(min_value=-90, max_value=90, allow_nan=False, allow_infinity=False),
                floats(allow_nan=False, allow_infinity=False)))
    else:
        raise ValueError("Position must be 2 or 3 dims")

    return pos


@composite
def bboxes(draw, dims=2):
    """
    https://tools.ietf.org/html/rfc7946#section-5
    """
    if dims is None:
        dims = draw(sampled_from([2, 3]))

    # Use 3 dim positions even if we only need 2
    pos1 = draw(positions(dims=3))
    pos2 = draw(positions(dims=3))
    lons, lats, zs = zip(pos1, pos2)

    if dims == 2:
        bbox = (min(lons), min(lats), max(lons), max(lats))
    elif dims == 3:
        bbox = (min(lons), min(lats), min(zs), max(lons), max(lats), max(zs))
    else:
        raise ValueError("dims must be 2 or 3")

    return bbox


@composite
def linestrings(draw):
    """
    https://tools.ietf.org/html/rfc7946#section-3.1.4
    """
    return draw(lists(positions(), min_size=2))


@composite
def linear_rings(draw, assert_validity=False):
    """
    https://tools.ietf.org/html/rfc7946#section-3.1.6
    """
    coords = draw(lists(positions(), min_size=4))
    coords.append(coords[0])
    if assert_validity:
        raise NotImplementedError('assert_validity not available yet')
    return coords


@composite
def geometries(draw, geom_types=None):
    """
    Questions
    ---------
    * When coordinates are composed of arrays of something,
    can those arrays be empty? Assume NO here (e.g.,
    MultiPoint is an array of *at least one* position.)

    * Need to add bbox and foreign members
    """
    if geom_types is None:
        # default to all
        geom_types = [
            'Point', 'LineString', 'Polygon',
            'MultiPoint', 'MultiLineString', 'MultiPolygon']

    geom_type = draw(sampled_from(geom_types))

    if geom_type == 'Point':
        coords = draw(positions())
    elif geom_type == 'LineString':
        coords = draw(linestrings())
    elif geom_type == 'Polygon':
        coords = draw(lists(linear_rings(), min_size=1))
    elif geom_type == 'MultiPoint':
        coords = draw(lists(positions(), min_size=1))
    elif geom_type == 'MultiLineString':
        coords = draw(lists(linestrings(), min_size=1))
    elif geom_type == 'MultiPolygon':
        coords = draw(lists(lists(linear_rings(), min_size=1), min_size=1))
    else:
        raise NotImplemented(geom_type)

    return {
        'type': geom_type,
        'coordinates': coords}


@composite
def geometry_collection(draw):
    """
    To Do
    -----
    * bbox and foreign members
    """
    geoms = draw(lists(geometries()))  # can be empty
    assume(len(geoms) != 1)  # avoid single geom
    return {
        'type': 'GeometryCollection',
        'geometries': geoms}


@composite
def properties(draw):
    return draw(dictionaries(
        keys=one_of(text(), integers()),
        values=one_of(
            text(),
            integers(),
            floats(allow_nan=False, allow_infinity=False),
            none())))


@composite
def features(draw):
    feature = {
        'type': 'Feature',
        'geometry': draw(one_of(geometries(), geometry_collection(), none())),
        'properties': draw(one_of(properties(), none()))}

    if draw(booleans()):
        feature['id'] = draw(one_of(
            integers(), text(), floats(allow_nan=False, allow_infinity=False)))

    if draw(booleans()):
        feature['bbox'] = draw(bboxes())

    # foreign members
    if draw(booleans()):
        key = draw(one_of(
            integers(), text(), floats(allow_nan=False, allow_infinity=False)))
        value = draw(one_of(
            integers(), text(), none(), floats(allow_nan=False, allow_infinity=False)))
        feature[key] = value

    return feature


@composite
def feature_collection(draw):
    """
    To do
    -----
    Foreign Members and bbox
    """
    feature_list = draw(lists(features()))
    return {
        'type': 'FeatureCollection',
        'features': feature_list}
