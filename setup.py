#!/usr/bin/env python3
"""nornir ipfabric inventory plugin"""
import setuptools

__author__ = "Gian Paolo Boarina"

with open("README.md", "r") as f:
    README = f.read()

setuptools.setup(
    name="nornir_ipfabric",
    version="2020.11.5.2",
    author=__author__,
    author_email="gp.boarina@gmail.com",
    description="nornir_ipfabric plugin for nornir",
    keywords="nornir ipfabric automation",
    license="Apache License, Version 2.0",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/routetonull/nornir_ipfabric",
    packages=setuptools.find_packages(),
    install_requires=[
        "nornir>=3.0.0a4,<4.0.0",
        "simplejson==3.17.2",
        "urllib3==1.25.11",
        "requests>=2.24.0",
    ],
    extras_require={},
    platforms="any",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    entry_points="""
    [nornir.plugins.inventory]
    IPFabricInventory=nornir_ipfabric.plugins.inventory:IPFabricInventory""",
)
