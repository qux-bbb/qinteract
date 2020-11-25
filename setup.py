from setuptools import setup, find_packages

setup(
    name='qinteract',
    version='0.1',
    author='qux-bbb',
    description='Process/Socket interactive',
    long_description=open('README.md', 'r', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages()
)