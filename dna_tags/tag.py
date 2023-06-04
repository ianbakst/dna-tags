from typing import Generator, List, Optional

from .base import Base
from .encoder import Encoder, NullEncoder


class Tag:
    """
    Object for a full tag. Contains a list of bases. Produced by a TagFactory object which
    governs the generation of Tags.
    """

    bases: List[Base]

    def __init__(self, bases: List[Base]):
        self.bases = bases

    def __repr__(self):
        return "".join(base.name for base in self.bases)

    @property
    def bin(self) -> str:
        """Binary representation of a tag."""
        return "".join(base.bin for base in self.bases)


class TagFactory:
    sequence_length: int
    message_length: int
    encoder: Encoder
    next_tag_number: int

    def __init__(
        self,
        *,
        total_length: Optional[int] = None,
        encoder: Optional[Encoder] = None,
        forbidden_tags: Optional[List[Tag]] = None,
        **encoder_options,
    ):
        self.next_tag_number = 0
        self.encoder = (
            NullEncoder(total_length)
            if encoder is None
            else encoder(total_length=total_length, **encoder_options)
        )

        self.sequence_length = self.encoder.total_length if total_length is None else total_length

    @property
    def next_tag_number(self):
        ntn = self._next_tag_number
        self._next_tag_number += 1
        return ntn

    @next_tag_number.setter
    def next_tag_number(self, value):
        self._next_tag_number = value

    def reset_tag_number(self):
        self.next_tag_number = 0

    def _create(self, tag_number: int) -> Tag:
        return Tag(self.encoder.encode(tag_number))

    def create_tag(self, tag_number: Optional[int] = None) -> Tag:
        if tag_number is None:
            tag_number = self.next_tag_number
        return self._create(tag_number)

    def create_tags(self, num: Optional[int] = None) -> Generator[Tag, None, None]:
        if num is None:
            num = self.encoder.max_tags
        for _ in range(num):
            tag_number = self.next_tag_number
            yield self._create(tag_number)

    def decode(self, tag: Tag) -> Tag:
        """
        Run the Tag through the encoder to apply any error correction/detection.
        :param tag:
        :return: The corrected DNA Tag (if it required correcting).
        :raises: DecodeError if an uncorrectable error is detected.
        """
        return Tag(self.encoder.decode(tag.bases))
