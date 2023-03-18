from collections.abc import Mapping, Sequence, Set
import operator

from . import utils


class Expression:
    def _parse_key(self, key):
        if isinstance(key, Boolean) or isinstance(key, Comparaison):
            return Filter(self, key)
        if key == '' or key is None:
            return Flatten(self)
        if isinstance(key,  str):
            return Key(self, key)
        if isinstance(key, Sequence):
            parsed = []
            for el in key:
                if isinstance(el, str):
                    parsed.append(j[el])
                else:
                    parsed.append(el)
            return ListSelect(self, key)
        if isinstance(key, Mapping):
            parsed = {}
            for k, el in key.items:
                if isinstance(el, str):
                    parsed[k] = j[el]
                else:
                    parsed[k] = el
            return DictSelect(self, key)
        if isinstance(key, Set):
            return DictSelect(self, {x: x for x in key})
        return Key(self, key)

    def __getitem__(self, keys):
        if not isinstance(keys, tuple):
            keys = (keys,)
        ikeys = iter(keys)
        result = j
        for key in ikeys:
            if isinstance(key, slice):
                # Consumes the rest of the keys
                right_keys = tuple(ikeys)
                result = Slice(key, result, j[right_keys]) 
            else:
                result = result._parse_key(key)
        if isinstance(self, Empty):
            return result
        return Pipe(self, result)

    def __rshift__(self, other):
        return Pipe(self, other)

    def __lt__(self, other):
        return Comparaison(self, other, operator.lt)

    def __le__(self, other):
        return Comparaison(self, other, operator.le) 

    def __gt__(self, other):
        return Comparaison(self, other, operator.gt)

    def __ge__(self, other):
        return Comparaison(self, other, operator.ge) 

    def __eq__(self, other):
        return Comparaison(self, other, operator.eq)

    def __ne__(self, other):
        return Comparaison(self, other, operator.ne) 

    def __or__(self, other):
        return Or(self, other) 

    def __and__(self, other):
        return And(self, other) 

    def __not__(self, other):
        return Not(self, other) 

    def __call__(self, doc):
        return doc


class UnaryOp(Expression):
    def __init__(self, expr):
        self._expr = expr

    def __str__(self):
        return f"{self.__class__.__name__}({self._expr})"


class BinOp(Expression):
    def __init__(self, left, right):
        self._left = left
        self._right = right

    def __str__(self):
        return f"{self.__class__.__name__}({self._left}, {self._right})"


Boolean = type('Boolean', (BinOp,), {})


class Or(Boolean):
    def __call__(self, doc):
        try:
            left = self._left(doc)
        except (KeyError, ValueError):
            left = False
        if left:
            return left
        else:
            return self._right(doc)


class And(Boolean):
    def __call__(self, doc):
        left = self._left(doc)
        if left:
            return self._right(doc)
        else:
            return left


class Not(Boolean):
    def __call__(self, doc):
        return not bool(self._expr(doc))



class Comparaison(Boolean):
    def __init__(self, left, right, op):
        self._left = left
        self._right = right
        self._op = op

    def __str__(self):
        return f"{self._op.__name__}({self._left}, {self._right})"

    def __call__(self, doc):
        left = self._left(doc)
        right = self._right(doc)
        return utils.compare(left, right, self._op)


class Flatten(UnaryOp):
    def __call__(self, doc):
        result = []
        if isinstance(doc, Sequence):
            for x in doc:
                result.extend(self(x))
        else:
            result.append(doc)
        return result


class Filter(BinOp):
    def __call__(self, doc):
        left = self._left(doc)
        if not isinstance(left, Sequence):
            raise ValueError
        result = []
        for x in left:
            if self._right(x):
                result.append(x)
        return result


class ListSelect(BinOp):
    def __call__(self, doc):
        left = self._left(doc)
        result = []
        for key in self._right:
            result.append(key(left))
        return result


class DictSelect(BinOp):
    def __call__(self, doc):
        left = self._left(doc)
        result = {}
        for key, value in self._right:
            result[key] = value(left)
        return result


class Key(BinOp):
    def __call__(self, doc):
        left = self._left(doc)
        return left[self._right]


class Slice(Expression):
    def __init__(self, slice_, left, right):
        self._slice = slice_
        self._left = left
        self._right = right

    def __str__(self):
        s = self._slice
        return f"Slice[{s.start}:{s.stop}:{s.step}]({self._left}, {self._right})"

    def __call__(self, doc):
        left = self._left(doc)
        if isinstance(left, Sequence):
            result = []
            for x in left[self._slice]:
                result.append(self._right(x))
        elif isinstance(left, Mapping):
            result = {}
            for k, v in left.items():
                if k >= self._slice.start and k < self._slice.stop:
                    result[k] = self._right(v)
        else:
            ValueError("Slice of a non-array: type(doc)")
        return result


class Pipe(BinOp):
    def __call__(self, doc):
        return self._right(self._left(doc))


class Empty(Expression):
    def __str__(self):
        return "J"


j = Empty()
