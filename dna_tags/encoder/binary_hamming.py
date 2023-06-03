from itertools import zip_longest
from math import ceil
from typing import List, Optional

from .encoder import DecodeError, Encoder, get_from_list
from ..base import Base


class BinaryHammingEncoder(Encoder):
    def __init__(
        self,
        message_bits: Optional[int] = None,
        total_length: Optional[int] = None,
        **kwargs,
    ):
        if (message_bits is None and total_length is None) or (
                message_bits is not None and total_length is not None
        ):
            raise ValueError("Must specify either message length, or total length.")
        if message_bits is not None:
            self.message_length = message_bits
            for i in range(2, 10):
                if self.message_length <= (2**i - i - 1):
                    self.parity = i
                    self.total_length = int(2 * ceil(0.5 * (self.parity + self.message_length)))
                    break
        if total_length is not None:
            self.total_length = 2 * total_length
            for i in range(2, 10):
                if self.total_length <= (2**i):
                    self.parity = i
                    self.message_length = self.total_length - self.parity - 1
                    break
        self.max_tags = 2**self.message_length

    @staticmethod
    def compute_parity(base_list: List[int]) -> int:
        return sum(base_list) % 2

    def encode(self, tag_number: int):
        if tag_number >= self.max_tags:
            raise ValueError(f"Tag number is out of range. Exceeds maximum tag number of {self.max_tags}.")
        tag_str = bin(tag_number)[2:]
        tag_str = "0" * (self.message_length - len(tag_str)) + tag_str
        bit_list = [i for i in tag_str]
        encoded = []
        for i in range(self.total_length):
            encoded.append(0 if i & (i - 1) == 0 else int(bit_list.pop(0)))

        for i, p in enumerate(range(self.parity, 0, -1)):
            parity_bit_list = get_from_list(encoded, order=p)
            encoded[2**i] = self.compute_parity(parity_bit_list)

        encoded[0] = self.compute_parity(encoded[1:])
        args = [iter([str(e) for e in encoded])] * 2
        return [Base(int("".join(c), 2)) for c in zip_longest(*args)]

    def decode(self, tag: List[Base]) -> List[Base]:
        tag_bits = [int(s) for s in "".join([b.bin for b in tag])]
        tag_bits.extend([0] * ((2 ** self.parity) - len(tag_bits)))
        correction = [self.compute_parity(get_from_list(tag_bits, order=p)) for p in range(self.parity, 0, -1)][::-1]

        overall_parity = self.compute_parity(tag_bits)
        if max(correction) == 1 and overall_parity == 0:
            raise DecodeError("Two or more errors detected.")
        if max(correction) != 0:
            pos_corr = int("".join([str(c) for c in correction]), 2)
            print(pos_corr)
            print(tag_bits)
            tag_bits[pos_corr] = (tag_bits[pos_corr] - max(correction)) % 2
            print(tag_bits)

        args = [iter([str(e) for e in tag_bits[: self.total_length]])] * 2
        return [Base(int("".join(c), 2)) for c in zip_longest(*args)]
