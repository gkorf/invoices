from setuptools import setup, find_packages
import os

PACKAGE_NAME = "invoices"

CURPATH = os.path.dirname(os.path.realpath(__file__))
VERSION_FILE = os.path.join(CURPATH, "version.txt")

with open(VERSION_FILE) as f:
    VERSION = f.read().strip()

INSTALL_REQUIRES = []

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    license='BSD-2-clause',
    description='Generates Greek tax invoices',
    packages=find_packages(),
    package_data={'': ['*.tex']},
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': {
            'invoice=invoices.invoice:main'
        }
    }
)
