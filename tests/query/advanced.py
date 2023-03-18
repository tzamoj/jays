from jays import j

from .utils import QueryTestCase


cases = {
    "proj_flat": QueryTestCase(
        query=j[:, ''],
        data=[[[1, 2], [3, 4]], [8, 9]],
        expected=[[1, 2, 3, 4], [8, 9]],
    ),
}
