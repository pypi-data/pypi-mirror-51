import os


def test_schematic(tmp_path):
    expected = """#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="test",
    version="0.1.0",
    description="Project built by Flaskerize",
    author="AJ Pryor",
    author_email="apryor6@gmail.com",
    url="https://github.com/apryor6/flaskerize",
    packages=find_packages(),
    install_requires=['thingy>0.3.0', 'widget>=2.4.3', 'doodad>4.1.0'],
)"""
    NAME = os.path.join(tmp_path, "test")
    COMMAND = f"""fz generate setup {NAME} --install-requires 'thingy>0.3.0' 'widget>=2.4.3' 'doodad>4.1.0' --author 'AJ Pryor' --author-email 'apryor6@gmail.com'"""
    os.system(COMMAND)

    outfile = os.path.join(tmp_path, "setup.py")
    assert os.path.isfile(outfile)
    with open(outfile, "r") as fid:
        content = fid.read()
    assert content == expected
