from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    README = f.read()

setup(
    name="pydbtcloud",
    version="0.0.3",
    description="Python SDK for dbt Cloud.",
    keywords="dbt",
    long_description=README,
    long_description_content_type='text/markdown',
    url="https://github.com/dwallace0723/py-dbt-cloud",
    author="David Wallace",
    author_email="dwallace0723@gmail.com",
    packages=find_packages(),
    install_requires=[
        'requests>=2.22.0'
    ],
    python_requires=">=3.7",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
)
