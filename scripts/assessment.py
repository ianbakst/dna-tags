import dna_tags as dna


if __name__ == "__main__":
    print("-----------------------------------")
    print("All Tag Sequences of 6 Bases:")
    tag_factory = dna.TagFactory(total_length=6)
    all_tags = [tag for tag in tag_factory.create_tags()]
    for tag in all_tags:
        print(tag)
    print(len(all_tags))
    print("___________________________________")
    print("Scheme 1: Binary Hamming")
    print("All tags of length 6")
    tag_factory = dna.TagFactory(total_length=6, encoder=dna.BinaryHammingEncoder)
    all_tags = [tag for tag in tag_factory.create_tags()]
    for tag in all_tags:
        print(tag)
    print(all_tags)

    print("1000+ Tags")
    tag_factory = dna.TagFactory(encoder=dna.BinaryHammingEncoder, message_bits=10)
    all_tags = [tag for tag in tag_factory.create_tags()]
    for tag in all_tags:
        print(tag)
    print(len(all_tags))
    print("-----------------------------------")
    print("Scheme 2: Quaternary Hamming")
    print("All tags of length 6")
    tag_factory = dna.TagFactory(
        encoder=dna.QuaternaryHammingEncoder, total_length=6, detect_double=False
    )
    all_tags = [tag for tag in tag_factory.create_tags()]
    for tag in all_tags:
        print(tag)
    print(len(all_tags))
    print("1000+ Tags")
