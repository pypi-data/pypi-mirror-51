# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.rst")) as f:
    long_description = f.read()

setup(
    name="pingtop",
    version="0.3.0",
    packages=find_packages(),
    description="Ping multiple servers and show the result in a top like terminal UI.",
    author="laixintao",
    author_email="laixintaoo@gmail.com",
    url="https://github.com/laixintao/pingtop",
    entry_points={"console_scripts": ["pingtop=pingtop:multi_ping"]},
    install_requires=["panwid", "click"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["IP", "ping", "icmp"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
)
