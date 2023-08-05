import re

from datetime import datetime
from operator import attrgetter


def find(predicate, seq):
    for element in seq:
        if predicate(element):
            return element
    return None


def get(iterable, **attrs):
    _all = all
    attrget = attrgetter

    # Special case the single element call
    if len(attrs) == 1:
        k, v = attrs.popitem()
        pred = attrget(k.replace('__', '.'))
        for elem in iterable:
            if pred(elem) == v:
                return elem
        return None

    converted = [
        (attrget(attr.replace('__', '.')), value)
        for attr, value in attrs.items()
    ]

    for elem in iterable:
        if _all(pred(elem) == value for pred, value in converted):
            return elem
    return None


def from_timestamp(timestamp):
    return datetime.strptime(timestamp, '%Y%m%dT%H%M%S.000Z')


def correct_tag(tag, prefix='#'):
    """Attempts to correct malformed Clash of Clans tags
    to match how they are formatted in game
    
    Example
    ---------
        ' 123aBc O' -> '#123ABC0'
    """
    return prefix + re.sub(r'[^A-Z0-9]+', '', tag.upper()).replace('O', '0')


def maybe_sort(seq, sort, itr=False, key=attrgetter('order')):
    """Returns list or iter based on itr if sort is false otherwise sorted
    with key defaulting to operator.attrgetter('order')
    """
    return (list, iter)[itr](n for n in sorted(seq, key=key)) \
        if sort else (list, iter)[itr](n for n in seq)
