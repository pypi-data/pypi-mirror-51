#!/usr/bin/env python3
import setuptools

with open("README.md", "rt") as readme_fp:
    long_description = readme_fp.read().strip()


setuptools.setup(
    name="mtprotoproxy",
    version="1.0.6",
    description="Async MTProto Proxy",
    long_description=long_description,
    url="https://github.com/alexbers/mtprotoproxy",
    author="Alexander Bersenev",
    author_email="bay@hackerdom.ru",
    maintainer="Alexander Bersenev",
    maintainer_email="bay@hackerdom.ru",
    license="MIT",
    packages=[],
    install_requires=[
        "pycryptodome~=3.6,!=3.6.2"
    ],
    extras_require={
        "uvloop": [
            "uvloop~=0.13.0"
        ]
    },
    scripts=[
        "mtprotoproxy.py", "mtprotoproxy"
    ],
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ]
)
