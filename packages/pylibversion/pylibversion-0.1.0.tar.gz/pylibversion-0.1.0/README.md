# pylibversion

[![CircleCI](https://circleci.com/gh/dbradf/pylibverions.svg?style=svg)](https://circleci.com/gh/dbradf/pylibverions)

A library to help manage versions in python libraries.

This package assumes that there is a main package with a `__init__.py` file with the `VERSION` defined as a tuple.

For example,

```python
VERSION = (0, 0, 1)
```

## Usage

### String based version

You can add a string based version as described in (PEP 396)[https://www.python.org/dev/peps/pep-0396/] to your
`__init__.py` file or in other locations with the `version_tuple_to_str` function:

```python
from pylibversion import version_tuple_to_str

VERSION = (0, 0, 1)
__version__ = version_tuple_to_str(VERSION)
```

### Include the version in setup.py

You can lookup the module version to include in setup.py with the `lookup_local_module_version` function:

```python
from pylibversion import lookup_local_module_version

...
setup(
    version=lookup_local_module_version(os.path.join("src", "module_name")),
    ...
)
```

### Compare current version to what is published to PyPi

You can compare the current version to what is published in PyPi with the `lookup_latest_version_in_pypi` function:

```python
def test_version_has_been_updated():
    module_name = "my_module"
    pypi_version = lookup_latest_version_in_pypi(module_name)
    my_version = my_module.__version__

    assert my_version != pypi_version
```
