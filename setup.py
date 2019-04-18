from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding = 'utf-8') as f:
    long_description = f.read()

setup(
    name = 'vkcoinapi',
    version = '1.2.2',
    packages = find_packages(),
    url = 'https://github.com/bixnel/vkcoinapi',
    license = 'MIT',
    author = 'Bixnel',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    install_requires = ['requests', 'websocket'],
    classifiers = ['Programming Language :: Python :: 3.6'],
)
