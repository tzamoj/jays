from .utils import QueryTestCase

from jays import j


cases = {
    "flatten_1": QueryTestCase(
        query=j[''],
        data=[[1, 2], [3, 4]],
        expected=[1, 2, 3, 4],
    ),
    "flatten_2": QueryTestCase(
        query=j[''],
        data=[[[1, 2], [3, 4]], [8, 9]],
        expected=[1, 2, 3, 4, 8, 9],
    ),
}
