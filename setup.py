
from setuptools import setup, find_packages

setup(
    name="issntools",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Saurabh Khanna",
    author_email="saurabh.khanna@pmb.ox.ac.uk",
    description="Tools for working with journal ISSNs.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
