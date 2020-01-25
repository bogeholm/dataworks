from setuptools import setup, find_namespace_packages

setup(
    name='dataworks',
    packages=find_namespace_packages(include=['mynamespace.*'])
)
