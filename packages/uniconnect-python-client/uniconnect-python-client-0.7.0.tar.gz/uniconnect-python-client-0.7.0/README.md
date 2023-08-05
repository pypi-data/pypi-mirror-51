![Build Status](https://travis-ci.org/uniconnect/uniconnect-python-client.svg?branch=master)

# Introduction

This package provides a client interface to query [uniconnect](https://uniconnect.io/)
a distributed SQL engine. It supports Python 2.7, 3.5, 3.6, and pypy.

# Installation

```
$ pip install uniconnect-python-client
```

# Quick Start

Use the DBAPI interface to query uniconnect:

```python
import uniconnect
conn=uniconnect.dbapi.connect(
    host='localhost',
    port=8080,
    user='the-user',
    catalog='the-catalog',
    schema='the-schema',
)
cur = conn.cursor()
cur.execute('SELECT * FROM system.runtime.nodes')
rows = cur.fetchall()
```

This will query the `system.runtime.nodes` system tables that shows the nodes
in the uniconnect cluster.

The DBAPI implementation in `uniconnect.dbapi` provides methods to retrieve fewer
rows for example `Cursorfetchone()` or `Cursor.fetchmany()`. By default
`Cursor.fetchmany()` fetches one row. Please set
`uniconnect.dbapi.Cursor.arraysize` accordingly.

# Basic Authentication
The `BasicAuthentication` class can be used to connect to a LDAP-configured uniconnect
cluster:
```python
import uniconnect
conn=uniconnect.dbapi.connect(
    host='coordinator url',
    port=8443,
    user='the-user',
    catalog='the-catalog',
    schema='the-schema',
    http_scheme='https',
    auth=uniconnect.auth.BasicAuthentication("principal id", "password"),
)
cur = conn.cursor()
cur.execute('SELECT * FROM system.runtime.nodes')
rows = cur.fetchall()
```

# Transactions
The client runs by default in *autocommit* mode. To enable transactions, set
*isolation_level* to a value different than `IsolationLevel.AUTOCOMMIT`:

```python
import uniconnect
from uniconnect import transaction
with uniconnect.dbapi.connect(
    host='localhost',
    port=8080,
    user='the-user',
    catalog='the-catalog',
    schema='the-schema',
    isolation_level=transaction.IsolationLevel.REPEATABLE_READ,
) as conn:
  cur = conn.cursor()
  cur.execute('INSERT INTO sometable VALUES (1, 2, 3)')
  cur.execute('INSERT INTO sometable VALUES (4, 5, 6)')
```

The transaction is created when the first SQL statement is executed.
`uniconnect.dbapi.Connection.commit()` will be automatically called when the code
exits the *with* context and the queries succeed, otherwise
`uniconnect.dbapi.Connection.rollback()' will be called.

# Running Tests

There is a helper scripts, `run`, that provides commands to run tests.
Type `./run tests` to run both unit and integration tests.

`uniconnect-python-client` uses [pytest](https://pytest.org/) for its tests. To run
only unit tests, type:

```
$ pytest tests
```

Then you can pass options like `--pdb` or anything supported by `pytest --help`.

To run the tests with different versions of Python in managed *virtualenvs*,
use `tox` (see the configuration in `tox.ini`):

```
$ tox
```

To run integration tests:

```
$ pytest integration_tests
```

They build a `Docker` image and then run a container with a uniconnect server:
- the image is named `uniconnect-server:${uniconnect_VERSION}`
- the container is named `uniconnect-python-client-tests-{uuid4()[:7]}`

The container is expected to be removed after the tests are finished.

Please refer to the `Dockerfile` for details. You will find the configuration
in `etc/`.

You can use `./run` to manipulate the containers:

- `./run uniconnect_server`: build and run uniconnect in a container
- `./run uniconnect_cli CONTAINER_ID`: connect the Java uniconnect CLI to a container
- `./run list`: list the running containers
- `./run clean`: kill the containers

# Development

Start by forking the repository and then modify the code in your fork.
Please refer to `CONTRIBUTING.md` before submitting your contributions.

Clone the repository and go inside the code directory. Then you can get the
version with `python setup.py --version`.

We recommend that you use `virtualenv` to develop on `uniconnect-python-client`:

```
$ virtualenv /path/to/env
$ /path/to/env/bin/active
$ pip install -r requirements.txt
```

For development purpose, pip can reference the code you are modifying in a
*virtualenv*:

```
$ pip install -e .[tests]
```

That way, you do not need to run `pip install` again to make your changes
applied to the *virtualenv*.

When the code is ready, submit a Pull Request.

# Need Help?

Feel free to create an issue as it make your request visible to other users and contributors.

If an interactive discussion would be better or if you just want to hangout and chat about the uniconnect Python client, you can join us on the *#uniconnect-python-client* channel on [Slack](https://uniconnect.slack.com).
