from setuptools import setup, find_packages


setup(
    author='Anna Movsisyan, Lusine Aghinyan, Ararat Kazarian, Hovhannes Hovhannisyan, Eduard Petrosyan',
    name='combogenius',
    description='A package designed to efficiently generate new product combinations using check information, and deliver combo suggestions to business partners via email.',
    version='0.1.0',
    packages=find_packages(include=['combogenius','combogenius.*']),
) 