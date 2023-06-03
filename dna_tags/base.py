from enum import Enum


class Base(Enum):
    A = 0
    T = 1
    C = 2
    G = 3

    @classmethod
    def _missing_(cls, value: int):
        return cls(value % 4)

    @property
    def bin(self):
        bin_repr = bin(self.value)[2:]
        return "0" * (2 - len(bin_repr)) + bin_repr

    def __str__(self):
        return self.name

    def __add__(self, other):
        if isinstance(other, int):
            return self.value + other
        return self.value + other.value

    def __radd__(self, other):
        if other == 0:
            return self.value
        else:
            return self.__add__(other)

    def __mod__(self, other):
        return self.value % other

    def __sub__(self, other):
        other_num = other if isinstance(other, int) else other.value
        new = self.value - other_num
        if new < 0:
            new += 4
        return self.__class__(new)
