# Testing
Information on how to run the package's unit tests and integration tests.

## Unit tests
Run the package's unit tests:
```bash
python setup.py test
```

## Integration tests
To test the package's compatibility with a GraceDB server requires a superuser account on the server.

Run the integration tests for the Python package:
```bash
python setup.py integration_test
```

Run the integration tests for the command-line client:
```bash
python setup.py test --addops "ligo/gracedb/test/integration/test_cli.py"
```

## Test compatibility with different versions of Python

Install tox:
```bash
pip install tox
```

The current [tox configuration](../../../tox.ini) runs the tests with Python 2.7 and 3.4-3.7. If your system does not have one of those interpreters, it will be skipped.

Run all tests with all specified versions of Python:
```bash
tox
```

Run unit tests only:
```bash
tox -e $(tox -l | grep unit_test | paste -sd "," -)
```

Run integration tests only:
```bash
tox -e $(tox -l | grep integration_test | paste -sd "," -)
```

Run all tests with one version of Python:
```bash
tox -e $(tox -l | grep py27 | paste -sd "," -)
```
