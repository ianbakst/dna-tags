from abc import ABC, abstractmethod
from math import ceil
from typing import List, Optional

from .base import Base


class DecodeError(Exception):
    pass


def get_from_list(tag_list: list, order: int = 0) -> list:
    if order == 0:
        return tag_list
    new_list = []
    s = ceil(len(tag_list) / (2**order))
    for i in range((2**order)):
        if i % 2 == 1:
            new_list.extend(tag_list[s * i : s * (i + 1)])
    return new_list


def not_powers_of_2(tag: list) -> list:
    new_tag = []
    for i, t in enumerate(tag):
        if not (i & (i - 1) == 0):
            new_tag.append(t)
    return new_tag


class Encoder(ABC):
    total_length: int
    message_length: int
    parity: int

    @abstractmethod
    def __init__(
        self, message_length: Optional[int], total_length: Optional[int], detect_double: Optional
    ):
        pass

    @abstractmethod
    def encode(self, tag: List[Base]) -> List[Base]:
        pass

    @abstractmethod
    def decode(self, tag: List[Base]) -> List[Base]:
        pass


class NullEncoder(Encoder):
    def __init__(
        self,
        message_length: Optional[int] = None,
        total_length: Optional[int] = None,
        detect_double: bool = False,
    ):
        if (message_length is None and total_length is None) or (
            message_length is not None and total_length is not None
        ):
            raise ValueError("Must specify either message length, or total length.")
        self.total_length = message_length if total_length is None else total_length
        self.message_length = self.total_length
        self.parity = 0

    def encode(self, tag: List[Base]) -> List[Base]:
        return tag

    def decode(self, tag: List[Base]) -> List[Base]:
        return tag


class QuaternaryHammingEncoder(Encoder):
    def __init__(
        self,
        message_length: Optional[int] = None,
        total_length: Optional[int] = None,
        detect_double: bool = True,
    ):
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
                if total_length <= (2**i):
                    self.parity = i
                    self.message_length = self.total_length - self.parity
                    self.message_length -= 1 if self.detect_double else 0
                    break

    @staticmethod
    def compute_parity(base_list: List[Base]) -> Base:
        return Base(4 - sum(base_list) % 4)

    def encode(self, tag: List[Base]) -> List[Base]:
        if len(tag) != self.message_length:
            raise ValueError("Message passed is too long for given encoder.")
        encoded = []
        for i in range(self.total_length):
            encoded.append(Base(0) if i & (i - 1) == 0 else tag.pop(0))
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
