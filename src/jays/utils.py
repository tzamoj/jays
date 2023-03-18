from collections.abc import Sequence, Mapping
import operator


def compare(left, right, op):
    if isinstance(left, Sequence) and not isinstance(left, str):
        return (
            isinstance(right, Sequence) and len(left) == len(right)
            and all(compare(l, r, op) for l, r in zip(left, right))
        )

    if isinstance(left, Mapping):
        return (
            isinstance(right, Mapping) and compare(list(left.keys()), list(right.keys()), operator.eq)
            and all(compare(left[k], right[k], op) for k in left.keys())
        )

    return op(left, right)
