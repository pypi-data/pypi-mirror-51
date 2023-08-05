#!/usr/bin/env python

# from distutils.core import setup, Extension
from setuptools import setup, Extension

long_desc = "".join(open("README.md").readlines())


setup(
    name='genice_extra',
    version='1.0',
    description='Installs all extra plugins for GenIce.',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
    ],
    author='Masakazu Matsumoto',
    author_email='vitroid@gmail.com',
    url='https://github.com/vitroid/genice-extra/',
    keywords=['genice'],
    install_requires=['genice-vpython>=0.4',
                      'genice-rdf>=0.3',
                      'genice-svg>=0.4',
                      'genice-twist>=0.1',
                      'genice-cif>=0.2',
                      'GenIce>=1.0rc5',
                      ],

    license='MIT',
)
