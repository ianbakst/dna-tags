import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dna_tags",
    version="0.1.0",
    author="Ian N. Bakst, Ph.D.",
    author_email="ian.bakst@gmail.com",
    description="DNA Tagging with Error Correction.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ianbakst/dna-tags",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
