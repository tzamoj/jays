from .utils import QueryTestCase

from jays import j


cases = {
    "select_dict_1": QueryTestCase(
        query=j["foo"],
        data={"foo": {"bar": "baz"}},
        expected={"bar": "baz"},
    ),
    "select_dict_2": QueryTestCase(
        query=j["foo", "bar"],
        data={"foo": {"bar": "baz"}},
        expected="baz",
    ),
    "select_dict_2_piped": QueryTestCase(
        query=j["foo"]["bar"],
        data={"foo": {"bar": "baz"}},
        expected="baz",
    ),
    "select_seq_1": QueryTestCase(
        query=j[1],
        data=[{"a": 1, "b": 2}, {"a": 2, "b": 4}],
        expected={"a": 2, "b": 4},
    ),
    "select_seq_2": QueryTestCase(
        query=j[1, 2],
        data=[[1, 2, 3], [4, 5, 6]],
        expected=6,
    ),
}
