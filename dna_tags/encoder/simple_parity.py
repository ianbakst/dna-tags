from itertools import zip_longest
from typing import List, Optional

from .encoder import DecodeError, Encoder
from ..base import Base


class SimpleParityEncoder(Encoder):
    def __init__(self, message_length: Optional[int] = None, total_length: Optional[int] = None):
        if (message_length is None and total_length is None) or (
            message_length is not None and total_length is not None
        ):
            raise ValueError("Must specify either message length, or total length.")

        if message_length is not None:
            self.message_length = message_length
            self.total_length = self.message_length + 1
        if total_length is not None:
            self.total_length = total_length
            self.message_length = self.total_length - 1
        self.max_tags = 4**self.message_length

    @staticmethod
    def compute_parity(base_list: List[Base]) -> Base:
        return Base(4 - sum(base_list) % 4)

    def encode(self, tag_number: int) -> List[Base]:
        if tag_number >= self.max_tags:
            raise ValueError(
                f"Tag number is out of range. Exceeds maximum tag number of {self.max_tags}."
            )
        tag_str = bin(tag_number)[2:]
        tag_str = "0" * (2 * self.message_length - len(tag_str)) + tag_str
        args = [iter(tag_str)] * 2
        bases = [Base(int("".join(c), 2)) for c in zip_longest(*args)]
        return bases + [self.compute_parity(bases)]

    def decode(self, tag: List[Base]) -> List[Base]:
        if self.compute_parity(tag[:-1]) != tag[-1]:
            raise DecodeError("A single-base error has been detected!")
        return tag[:-1]
