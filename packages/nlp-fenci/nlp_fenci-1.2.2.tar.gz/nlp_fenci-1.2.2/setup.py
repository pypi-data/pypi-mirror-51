# -*- coding: utf-8 -*-
# python lib_setup.py sdist bdist_wheel upload
import os

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements

import setuptools

dir_path = os.path.dirname(os.path.realpath(__file__))


def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nlp_fenci",
    version="1.2.2",
    author="cx",
    author_email="sharpcx@live.com",
    description="分词工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SharpCX/sougou_fenci.git",
    packages=["bin","fenci"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/sougou_fenci', 'bin/baidu_fenci'],
    install_requires=load_requirements(os.path.join(dir_path, 'requirements.txt'))
)
