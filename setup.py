import sys
import re

from setuptools.command.test import test as TestCommand
from setuptools import setup
# from setuptools import find_packages


metadata = dict(
    re.findall("__([a-z]+)__ = '([^']+)'", open('fity3.py').read()))


README = open('README.rst').readlines()[3:]

description = ' '.join(README[:README.index('\n')]).replace('\n', '')
long_description = ''.join(README[README.index('\n'):])


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='python-fity3',
    version=metadata['version'],
    author='Andy Gayton',
    author_email='andy@thecablelounge.com',
    # install_requires=requirements,
    # packages=find_packages(),
    py_modules=['fity3'],
    url='https://github.com/cablehead/python-fity3',
    license='MIT',
    description=description,
    long_description=open('README.rst').read(),
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)
