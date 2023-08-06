# osis2usfm

[![Build Status](https://travis-ci.org/bbelyeu/osis2usfm.svg?branch=master)](https://travis-ci.org/bbelyeu/osis2usfm)
[![Coverage Status](https://coveralls.io/repos/github/bbelyeu/osis2usfm/badge.svg?branch=master)](https://coveralls.io/github/bbelyeu/osis2usfm?branch=master)

## Requirements

This project requires Python 3 (tested with 3.3-3.7)

## Installation

To install it, simply run

    pip install osis2usfm

## Usage

Import it and wrap app

    from osis2usfm import convert

    osis = ['Gen.1.1', '2Pet.1.1', 'John.1.1']
    usfms = convert(osis)
    print(usfms)
    >>> ['GEN.1.1', '2PE.1.1', 'JHN.1.1']

## Development

This project was written and tested with Python 3. Our builds currently support Python 3.3 to 3.7.

Install Python 3 into your system. Create a virtualenv, and then install the requirements with:

``` base
pip install -r requirements.txt
```

### Running tests

``` bash
./linters.sh && coverage run setup.py test
```

### Before committing any code

We have a pre-commit hook each dev needs to setup.
You can symlink it to run before each commit by changing directory to the repo and running

``` bash
cd .git/hooks
ln -s ../../pre-commit pre-commit
cd -
```
