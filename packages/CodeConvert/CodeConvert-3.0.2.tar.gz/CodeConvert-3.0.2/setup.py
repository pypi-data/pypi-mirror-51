# -*- coding: utf-8 -*-

from setuptools import setup


version = '3.0.2'


setup(
    name='CodeConvert',
    version=version,
    keywords='CodeConvert unicode utf8 utf-8 gbk latin1 raw_unicode_escape',
    description='Code Convert for Python 2.x for Humans™',
    long_description=open('README.rst').read(),

    url='https://github.com/Brightcells/CodeConvert',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['CodeConvert'],
    py_modules=[],
    install_requires=['six'],

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
