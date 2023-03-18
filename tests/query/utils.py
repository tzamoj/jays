from dataclasses import dataclass
from typing import Any

import jays.expressions


@dataclass
class QueryTestCase:
    query: jays.expressions.Expression
    data: Any
    expected: Any
