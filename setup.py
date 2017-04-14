# -*- coding: utf-8 -*-
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="tracboat",
    version='0.2.0a0',
    description="Trac to GitLab migration toolbox",
    long_description=long_description,
    author="Federico Ficarelli",
    author_email="federico.ficarelli@gmail.com",
    url="https://github.com/nazavode/tracboat",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    install_requires=[
        'peewee',
        'psycopg2',
        'six',
        'click',
        'toml',
        'pymongo',
    ],
    entry_points={
        'console_scripts': [
            'tracboat=tracboat.cli:main',
        ],
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ],
    keywords='trac gitlab migration',
)
