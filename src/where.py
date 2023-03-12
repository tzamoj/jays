import operator


class Expression:
    def __getitem__(self, key):
        if isinstance(key, Boolean) or isinstance(key, Comparaison):
            return Filter(self, key)
        if key == '':
            return Flatten(self, None)
        if key == '*':
            return ListProjection(self)
        if key == '**':
            return DictProjection(self)
        if isinstance(key, list):
            parsed = []
            for el in key:
                if isinstance(el, str):
                    parsed.append(j[el])
                else:
                    parsed.append(el)
            return ListSelect(self, key)
        if isinstance(key, dict):
            parsed = {}
            for k, el in key.items:
                if isinstance(el, str):
                    parsed[k] = j[el]
                else:
                    parsed[k] = el
            return DictSelect(self, key)
        if isinstance(key, set) or isinstance(key, tuple):
            return DictSelect(self, {x: x for x in key})
        return Key(self, key)

    # def __getattr__(self, key):
        # self <- SubExpression -> function   if not a projection
        # self -> function   if a projection

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
        return OR(self, other) 

    def __and__(self, other):
        return AND(self, other) 

    def __not__(self, other):
        return NOT(self, other) 

    def __call__(self, doc):
        return parse(self, doc)


Empty = type('Empty', (Expression,), {})
Boolean = type('Boolean', (Expression,), {})
OR = type('OR', (Boolean,), {})
AND = type('AND', (Boolean,), {})
NOT = type('NOT', (Boolean,), {})


class UnaryOp(Expression):
    def __init__(self, expr):
        self._expr = expr


class BinOp(Expression):
    def __init__(self, left, right):
        self._left = left
        self._right = right


class Projection(Expression):
    def __init__(self, left):
        self._left = left
        self._right = j

    def __getitem__(self, key):
        self._right = self._right[key]
        return self


class Comparaison(Boolean):
    def __init__(self, left, right, op):
        self._left = left
        self._right = right
        self._op = op


Flatten = type('Flatten', (UnaryOp,), {})
Filter = type('Filter', (BinOp,), {})
ListProjection = type('ListProjection', (Projection,), {})
ListSelect = type('ListSelect', (BinOp,), {})
DictProjection = type('DictProjection', (Projection,), {})
DictSelect = type('DictSelect', (BinOp,), {})
Key = type('Key', (BinOp,), {})
Pipe = type('Pipe', (BinOp,), {})


def parse(expr, doc):
    if isinstance(expr, Empty):
        return doc

    if isinstance(expr, str):
        return parse(j[expr], doc)

    if isinstance(expr, Pipe):
        return _pipe(expr, doc)

    if isinstance(expr, Flatten):
        return _flatten(expr._left, doc)

    if isinstance(expr, ListProjection):
        return _project_list(expr, doc)

    if isinstance(expr, DictProjection):
        return _project_dict(expr, doc)

    if isinstance(expr, ListSelect):
        return _select_list(expr, doc)

    if isinstance(expr, DictSelect):
        return _select_dict(expr, doc)

    if isinstance(expr, Key):
        return _key(expr, doc)

    if isinstance(expr, Comparaison):
        return _comparaison(expr, doc)

    if isinstance(expr, OR):
        return _or(expr, doc)

    if isinstance(expr, AND):
        return _and(expr, doc)

    if isinstance(expr, NOT):
        return _not(expr, doc)

    if isinstance(expr, Filter):
        return _filter(expr, doc)


def _pipe(expr, doc):
    return parse(expr._right, parse(expr._left, doc))


def _flatten(expr, doc):
    result = []
    if isinstance(doc, list):
        for x in doc:
            result.extend(parse(expr, x))
    else:
        result.append(doc)
    return result


def _project_list(expr, doc):
    left = parse(expr._left, doc)
    result = []

    if isinstance(left, list):
        for x in left:
            result.append(parse(expr._right, x))
    elif isinstance(left, dict):
        for x in left.values():
            result.append(parse(expr._right, x))
    else:
        raise ValueError
    return result


def _project_dict(expr, doc):
    left = parse(expr._left, doc)

    if not isinstance(left, dict):
        raise ValueError

    result = {}
    for k, v in left.items():
        result[k] = parse(expr._right, v)
    return result


def _select_list(expr, doc):
    left = parse(expr._left, doc)
    result = []
    for key in expr._right:
        result.append(parse(key, left))
    return result


def _select_dict(expr, doc):
    left = parse(expr._left, doc)
    result = {}
    for key, value in expr._right:
        result[key] = parse(value, left)
    return result


def _key(expr, doc):
    left = parse(expr._left, doc)
    return left[expr._right]


def _or(expr, doc):
    left = parse(expr._left, doc)
    if left:
        return left
    else:
        return parse(expr._right, doc)


def _and(expr, doc):
    left = parse(expr._left, doc)
    if left:
        return parse(expr._right, doc)
    else:
        return left


def _not(expr, doc):
    return not bool(parse(expr._expr, doc))


def _comparaison(expr, doc):
    left = parse(expr._left, doc)
    right = parse(expr._right, doc)
    return _compare(left, right, expr._op)


def _compare(left, right, op):
    if isinstance(left, list):
        return (
            isinstance(right, list) and len(left) == len(right)
            and all(_compare(l, r, op) for l, r in zip(left, right))
        )
    if isinstance(left, dict):
        return (
            isinstance(right, dict) and _compare(list(left.keys()), list(right.keys()), operator.eq)
            and all(_compare(left[k], right[k], op) for k in left.keys())
        )
    return op(left, right)


def _filter(expr, doc):
    left = parse(expr._left, doc)
    if not isinstance(left, list):
        raise ValueError
    result = []
    for x in left:
        if parse(expr._right, x):
            result.append(x)
    return result


j = Empty()
