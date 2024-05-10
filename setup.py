from setuptools import setup, find_packages
from pathlib import Path
this_directory=Path(__file__).parent
long_description=(this_directory / "README.md").read_text()

setup(
    author='Anna Movsisyan, Lusine Aghinyan, Ararat Kazarian, Hovhannes Hovhannisyan, Eduard Petrosyan',
    name='combogenius',
    description='A package designed to efficiently generate new product combinations using check information, and deliver combo suggestions to business partners via email.',
    version='0.2.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(include=['combogenius','combogenius.*']),
) 