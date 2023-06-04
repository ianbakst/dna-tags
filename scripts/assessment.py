import dna_tags as dna


def print_all_tags(tf: dna.TagFactory):
    all_tags = [tag for tag in tf.create_tags()]
    print(f"Total number of tags: {len(all_tags)}")
    for tag in all_tags:
        print(tag, end=", ")
    print("\n")


if __name__ == "__main__":
    print("-----------------------------------")
    print("All Tag Sequences of 6 Bases:")
    print_all_tags(dna.TagFactory(total_length=6))
    print("___________________________________")
    print("Scheme 1: Binary Hamming")
    print("All tags of length 6")
    print_all_tags(dna.TagFactory(total_length=6, encoder=dna.BinaryHammingEncoder))
    print("1000+ Tags")
    print_all_tags(dna.TagFactory(encoder=dna.BinaryHammingEncoder, message_bits=10))

    print("-----------------------------------")
    print("Scheme 2: Quaternary Hamming")
    print("All tags of length 6")
    print_all_tags(
        dna.TagFactory(encoder=dna.QuaternaryHammingEncoder, total_length=6, detect_double=False)
    )

    print("1000+ Tags")
    print_all_tags(
        dna.TagFactory(encoder=dna.QuaternaryHammingEncoder, message_length=5, detect_double=False)
    )
