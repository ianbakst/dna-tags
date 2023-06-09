from itertools import zip_longest
from typing import List, Optional

from .encoder import DecodeError, Encoder, get_from_list
from ..base import Base


class QuaternaryHammingEncoder(Encoder):
    """ """

    def __init__(
        self,
        message_length: Optional[int] = None,
        total_length: Optional[int] = None,
        detect_double: bool = True,
    ):
        """
        Initialize the Quaternary Hamming Encoder.
        :param message_length: Total Message Length in Bases
        :param total_length: Total Tag length (including check bases)
        :param detect_double: Whether an additional base will be added to be able to detect double base substitution
                              errors
        """
        self.detect_double = detect_double
        if (message_length is None and total_length is None) or (
            message_length is not None and total_length is not None
        ):
            raise ValueError("Must specify either message length, or total length.")
        if message_length is not None:
            self.message_length = message_length
            for i in range(2, 10):
                if message_length <= (2**i - i - 1):
                    self.parity = i
                    self.total_length = self.parity + message_length
                    self.total_length += 1 if self.detect_double else 0
                    break
        if total_length is not None:
            self.total_length = total_length
            for i in range(2, 10):
                if total_length <= (2**i - (0 if self.detect_double else 1)):
                    self.parity = i
                    self.message_length = self.total_length - self.parity
                    self.message_length -= 1 if self.detect_double else 0
                    break
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
        encoded = []
        for i in range(self.total_length + (0 if self.detect_double else 1)):
            encoded.append(Base(0) if i & (i - 1) == 0 else bases.pop(0))
        encoded.extend([Base(0)] * ((2**self.parity) - len(encoded)))
        for i, p in enumerate(range(self.parity, 0, -1)):
            parity_base_list = get_from_list(encoded, order=p)
            encoded[2**i] = Base(self.compute_parity(parity_base_list))
        if self.detect_double:
            encoded[0] = Base(4 - sum(encoded[1:]) % 4)
        else:
            encoded.pop(0)
        return encoded[: self.total_length]

    def decode(self, tag: List[Base]) -> List[Base]:
        if not self.detect_double:
            tag.insert(0, Base(0))
        tag.extend([Base(0)] * ((2**self.parity) - len(tag)))
        correction = [sum(get_from_list(tag, order=p)) % 4 for p in range(self.parity, 0, -1)][
            ::-1
        ]
        overall_parity = sum(tag) % 4 if self.detect_double else max(correction)
        set_corr = set(correction)
        if len(set_corr) > 2 or max(correction) != overall_parity:
            raise DecodeError("Two or more errors detected.")
        if max(correction) != 0:
            pos_corr = int("".join([str(int(c / max(correction))) for c in correction]), 2)
            tag[pos_corr] -= max(correction)
        return tag[(0 if self.detect_double else 1) :][: self.total_length]
