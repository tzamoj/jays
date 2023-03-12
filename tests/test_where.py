doc = {
    "foo": [
        {"a": "char", "b": "char"},
        {"a": 2, "b": 1},
        {"a": 1, "b": 2},
    ]
}

j["foo"][j["a"] < j["b"]]
