from setuptools import find_packages, setup

setup(
    name="u8_encode",
    version="0.1.0",
    description="A package for encoding and decoding data for PIR experiments.",
    author="dc",
    packages=find_packages(),
    install_requires=[
        "pandas",
    ],
)
