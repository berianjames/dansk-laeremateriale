from setuptools import find_packages, setup

setup(
    name="DanskLaeremateriale",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "nltk",
        "PyMuPDF",
        "marvin",
    ],
)
