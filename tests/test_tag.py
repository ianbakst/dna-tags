from itertools import product
import pytest

import dna_tags as dna


@pytest.mark.parametrize(
    "tot_len,encoder",
    [(i, e) for i, e in product(range(4, 10), [dna.NullEncoder, dna.BinaryHammingEncoder, dna.QuaternaryHammingEncoder])]
)
def test_tag_length(tot_len, encoder):
    tf = dna.TagFactory(total_length=tot_len, encoder=encoder)
    assert len(tf.create_tag()) == tot_len


@pytest.mark.parametrize(
    "tot_len,encoder",
    [(i, dna.QuaternaryHammingEncoder) for i in range(4, 10)]
)
def test_tag_length_no_dd(tot_len, encoder):
    tf = dna.TagFactory(total_length=tot_len, encoder=encoder, detect_double=False)
    assert len(tf.create_tag()) == tot_len


@pytest.mark.parametrize(
    "tot_len,encoder",
    [(i, e) for i, e in product(range(4, 10), [dna.NullEncoder, dna.BinaryHammingEncoder, dna.QuaternaryHammingEncoder])]
)
def test_tag_uniqueness(tot_len, encoder):
    all_tags = [t for t in dna.TagFactory(total_length=tot_len, encoder=encoder).create_tags()]
    assert len(set(all_tags)) == len(all_tags)
