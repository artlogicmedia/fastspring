# fastspring

This is a simple Python module designed to interact with the FastSpring ordering
and subscription API. This module requires [xmltodict][1] to work. Data is
passed into and returned from the API object in dicts.

## Installation

```bash
$ git clone https://github.com/artlogicmedia/fastspring.git
$ cd fastspring/python-2
$ sudo python setup.py install
```

## Methods

Each method of the API class corresponds directly to an API endpoint. The
[official FastSpring API documentation][2] is the best reference for
understanding what does what. More explicit documentation will be forthcoming
here in the future.

## Python 2 & Python 3

There are both Python 2 and Python 3 variants available in this repository.
Please note that the Python 3 variant is untested as of this writing, and may
contain bugs not present in the Python 2 version.

[1]: https://github.com/martinblech/xmltodict/
[2]: https://github.com/fastspring/fastspring-api/