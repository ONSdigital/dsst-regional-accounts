"""Setup script for creating package from code."""
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='dsst_regional_accounts',
    version='0.1.0-dev0',
    description='DSST regional accounts project',
    url='https://github.com/ONSdigital/dsst-regional-accounts',
    packages=find_packages(),
    zip_safe=False,
    install_requires=requirements,
    include_package_data=True,
)