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
    print("All Tag Sequences of 6 Bases in Hamming4 Scheme:")
    tag_factory = dna.TagFactory(
        total_length=6, encoder=dna.encoder.DoubleErrorCorrectionEncoder
    )
    print(
        tag_factory.encoder.parity,
        tag_factory.encoder.message_length,
        tag_factory.encoder.total_length,
    )
    all_tags = [tag for tag in tag_factory.create_tags()]
    for t in all_tags:
        tt = t
        print(tt)
    print(len(all_tags))
    print("-----------------------------------")

