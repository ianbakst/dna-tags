# DNA Tags
### A tool for generating DNA tags of various schemes of error detection/correction

## Quick Start
1. Clone this repository onto your local computer:`git clone https://github.com/ianbakst/dna-tags.git`
2. In a terminal, enter the directory the repository was cloned into: `cd dna-tags`
3. Be sure you're using Python 3.9 or greater. Create a virtual environment (optional, but recommended)
4. Install the package: `pip install .`

## Basic Workflow:
At the core of the package is the TagFactory object, which controls the generation of tags.
The TagFactory keeps track of which

```python
import dna_tags as dna

# Initialize a tag factory object
tag_factory = dna.TagFactory(total_length=6, encoder=dna.BinaryHammingEncoder)

# Generate a single tag of the first available number
tag1 = tag_factory.create_tag()

# Generate a tag of an arbitrary number
tag2 = tag_factory.create_tag(27)

# Generate the next 10 tags: (returns a generator object)
tags10 = [t for t in tag_factory.create_tags(10)]

# reset the next generated tag number to 0
tag_factory.reset_tag_number()

# Generate all tags in a given scheme/size
tags_all = [t for t in tag_factory.create_tags()]
```

## Encoders
Encoders are available to address the application of an error detection or correction scheme.
Currently, there are 3 encoders available:

### Null Encoder
The `NullEncoder` object is the standard/default encoder. It does not encode with any error correction.
The `NullEncoder` returns the direct number-to-Base translation of the tag. Tags produced by this
encoder are not at all substitution-safe.

### Binary Hamming Encoder
The `BinaryHammingEncoder` encodes the tag in a Binary Hamming scheme. This involves considering
each base as 2 bits (A = 00, T = 01, C = 10, G = 11), and producing Hamming Code for that
sequence of bits. Since Bases (and subsequently Tags) exclusively consist of an even number of bits,
we can utilize the overall parity bit (double error detection) of a SECDEC code.

This is important since the Binary Hamming code is only error-correcting to single-bit errors.
However, only two-thirds of possible base substitutions are single-bit errors, while the other
third is a double bit error (A -> G = 00 -> 11). Thus, implementing this encoder is not guaranteed to
be self-correcting on all base substitution errors. It will, however, at least detect all errors,
and be able to correct two-thirds of them.

### Quaternary Hamming Encoder
The `QuaternaryHammingEncoder` encodes the tag in a Quaternary Hamming (H4) scheme, which is
100% error correcting to **all** single base substitutions. There are two implementations
of this scheme: with and without double error detection (toggled with the `detect_double` parameter).
Adding double error detection increases the tag size by one base. However, without double error
detection, the scheme cannot detect, or be guaranteed to correct tags with 2 or more errors.
