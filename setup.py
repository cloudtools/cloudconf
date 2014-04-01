import os
import sys
from setuptools import setup, find_packages

src_dir = os.path.dirname(__file__)

def read(filename):
    full_path = os.path.join(src_dir, filename)
    with open(full_path) as fd:
        return fd.read()


if __name__ == '__main__':
    setup(
        name='cloudconf',
        version='0.1.1',
        author='Michael Barrett',
        author_email='loki77@gmail.com',
        license="New BSD license",
        url="https://github.com/phobologic/cloudconf",
        description="Simple helper library for ubuntu's cloudinit.",
        long_description=read('README.rst'),
        classifiers=[
            "License :: OSI Approved :: BSD License",
            "Development Status :: 3 - Alpha"],
        packages=find_packages(),
    )
