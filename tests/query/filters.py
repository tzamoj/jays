from .utils import QueryTestCase

from jays import j


cases = {
    "select_filter": QueryTestCase(
        query=j["foo", j["a"] < j["b"]],
        data={"foo": [{"a": "char", "b": "char"}, {"a": 2, "b": 1}, {"a": 1, "b": 2}]},
        expected=[{"a": 1, "b": 2}],
    ),
}
