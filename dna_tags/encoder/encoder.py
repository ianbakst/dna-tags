from abc import ABC, abstractmethod
from itertools import zip_longest
from math import ceil
from typing import List, Optional

from ..base import Base


class DecodeError(Exception):
    pass


class Encoder(ABC):
    total_length: int
    message_length: int
    parity: int
    max_tags: int

    @abstractmethod
    def __init__(self, total_length: Optional[int], **kwargs):
        pass

    @abstractmethod
    def encode(self, tag: List[Base]) -> List[Base]:
        pass

    @abstractmethod
    def decode(self, tag: List[Base]) -> List[Base]:
        pass


class NullEncoder(Encoder):
    def __init__(self, total_length: Optional[int] = None, **kwargs):
        if total_length is None:
            raise ValueError("Must specify tag length.")
        self.total_length = total_length
        self.message_length = self.total_length
        self.parity = 0
        self.max_tags = 4**self.message_length

    def encode(self, tag_number: int) -> List[Base]:
        if tag_number >= 4**self.message_length:
            raise ValueError(
                f"Tag number is out of range. Exceeds maximum tag number of {4**self.message_length}."
            )
        tag_str = bin(tag_number)[2:]
        tag_str = "0" * (2 * self.total_length - len(tag_str)) + tag_str
        args = [iter(tag_str)] * 2
        return [Base(int("".join(c), 2)) for c in zip_longest(*args)]

    def decode(self, tag: List[Base]) -> List[Base]:
        return tag


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
