# Integration testing for ligo-gracedb
*Last updated 15 Jan 2019*

## General information
The default GraceDB service for tests is at https://gracedb-test.ligo.org/api/
To change this, you can add 

    TEST_SERVICE={url}

to the beginning of any of the above commands. Or, you can set TEST_SERVICE
in your environment and then run these commands:

    export TEST_SERVICE={url}

To use custom test data, set TEST_DATA_DIR. (see base.py and test.sh for more info about test data)

## Running integration tests
To run all integration tests:

```bash
python setup.py integration_test
```

To only run certain ones, you can do something like

```bash
# For standard test classes
python setup.py integration_test -s ligo.gracedb.test.integration.test_superevents.TestSuperevents

# For specially ordered test suites
python setup.py integration_test -s ligo.gracedb.test.integration.test_voevents.VOEventTestSuite
```

## Adding integration tests
In ligo/gracedb/test/integration/__init__.py, add the following:

```python
# Import new test class or suite
from .test_new import NewTestClass, NewTestSuite

# If it's a standard test class, add it to the list of test classes
testClasses = [..., NewTestClass]

# Or, for a suite, add it to the list of test suites
test_suites = [..., NewTestSuite]
```

## Command-line interface integration tests
If using a virtualenv with ligo-gracedb installed, do `ligo/gracedb/test/integration/test.sh`.

Otherwise, go to the root of this repository and run

```bash
PYTHONPATH=. GRACEDB='python bin/gracedb' ligo/gracedb/test/integration/test.sh 
```
