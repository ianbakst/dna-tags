from itertools import product
from random import choices
import pytest

import dna_tags as dna


@pytest.mark.parametrize(
    "input_int,expected",
    [(0, dna.Base.A), (1, dna.Base.T), (2, dna.Base.C), (3, dna.Base.G), (4, dna.Base.A)],
)
def test_base_init_by_int(input_int, expected):
    assert dna.Base(input_int) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [("A", dna.Base.A), ("T", dna.Base.T), ("C", dna.Base.C), ("G", dna.Base.G)],
)
def test_base_init_by_name(input_str, expected):
    assert dna.Base[input_str] == expected


@pytest.mark.parametrize(
    "input1,input2,result",
    [(dna.Base(i), dna.Base(j), i + j) for i, j in product([0, 1, 2, 3], [0, 1, 2, 3])],
)
def test_base_add(input1, input2, result):
    assert input1 + input2 == result


@pytest.mark.parametrize(
    "input_list,result",
    [([dna.Base(b) for b in c], sum(c)) for c in [choices([0, 1, 2, 3], k=i) for i in range(10)]],
)
def test_base_sum(input_list, result):
    assert sum(input_list) == result
