from .utils import QueryTestCase

from jays import j


cases = {
    "or_left": QueryTestCase(
        query=j["foo"] | j["bar"],
        data={"foo": {"bar": "baz"}},
        expected={"bar": "baz"},
    ),
    "or_right": QueryTestCase(
        query=j["foo"] | j["bar"],
        data={"bar": "value"},
        expected="value",
    ),
    "or_both": QueryTestCase(
        query=j["foo"] | j["bar"],
        data={"foo": "foo-value", "bar": "bar-value"},
        expected="foo-value",
    ),
    "or_chain": QueryTestCase(
        query=j["foo"] | j["bar"] | j["baz"],
        data={"whatever": 1, "baz": "baz-value"},
        expected="baz-value",
    ),
    "no_override": QueryTestCase(
        query=j["override"] | j["a", -1],
        data={"a": [1, "two"]},
        expected="two",
    ),
    "override": QueryTestCase(
        query=j["override"] | j["a", -1],
        data={"a": [1, "two"], "override": 2},
        expected=2,
    ),
}
