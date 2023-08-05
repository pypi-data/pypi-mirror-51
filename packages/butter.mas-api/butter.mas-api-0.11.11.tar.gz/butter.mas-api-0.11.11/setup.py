# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md', encoding="utf8") as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='butter.mas-api',
    version='0.11.11',
    description='Python Client API for Butter MAS platform',
    long_description_content_type='text/markdown',
    long_description=readme,
    author='Benny Megidish',
    author_email='bennymegk@gmail.com',
    url='https://github.com/benymeg/Butter.MAS.PythonAPI',
    install_requires=['requests'],
    #license=license,
    license='Apache-2.0',
    packages=find_packages(exclude=('tests', 'docs'))
)

''' how to deploy '''
# python setup.py sdist bdist_wheel
# python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# pip install --index-url https://test.pypi.org/simple/ --no-deps butter.mas-api

# python -m twine upload dist/*
# pip install -U butter.mas-api

''' how to generate documentation '''
# cd sphinx
# ./make html
# XCOPY ".\_build\html" "..\docs"