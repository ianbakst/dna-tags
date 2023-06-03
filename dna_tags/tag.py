from itertools import zip_longest
from typing import Generator, List, Optional

from .base import Base
from .encoder import Encoder, NullEncoder


class Tag:
    bases: List[Base]

    def __init__(self, bases: List[Base]):
        self.bases = bases

    def __repr__(self):
        return "".join(base.name for base in self.bases)


class TagFactory:
    sequence_length: int
    message_length: int
    encoder: Encoder
    next_tag_number: int

    def __init__(
        self,
        *,
        total_length: Optional[int] = None,
        message_length: Optional[int] = None,
        encoder: Optional[Encoder] = None,
        **encoder_options,
    ):
        if total_length is None and message_length is None:
            raise ValueError("Must specify at least overall_sequence_length or message_length")
        self.next_tag_number = 0
        self.encoder = (
            NullEncoder(total_length, message_length)
            if encoder is None
            else encoder(
                total_length=total_length, message_length=message_length, **encoder_options
            )
        )

        self.sequence_length = self.encoder.total_length if total_length is None else total_length
        self.message_length = (
            self.encoder.message_length if message_length is None else message_length
        )

    @property
    def next_tag_number(self):
        ntn = self._next_tag_number
        self._next_tag_number += 1
        return ntn

    @next_tag_number.setter
    def next_tag_number(self, value):
        self._next_tag_number = value

    def _create(self) -> Tag:
        n = self.next_tag_number
        binary_rep = bin(n)[2:]
        bin_str = "0" * (2 * self.message_length - len(binary_rep)) + binary_rep
        args = [iter(bin_str)] * 2
        bases = [Base(int("".join(c), 2)) for c in zip_longest(*args)]
        return Tag(self.encoder.encode(bases))

    def create_tags(self, num: Optional[int] = None) -> Generator[Tag, None, None]:
        if num is None:
            num = 4**self.message_length
        for _ in range(num):
            yield self._create()

    def decode(self, tag: Tag) -> Tag:
        return Tag(self.encoder.decode(tag.bases))
