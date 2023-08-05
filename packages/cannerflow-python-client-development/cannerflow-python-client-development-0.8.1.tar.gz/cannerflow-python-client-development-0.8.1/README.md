![Build Status](https://travis-ci.org/canner/cannerflow-python-client.svg?branch=master)

# Introduction

This package provides a client interface to query Cannerflow
a distributed SQL engine. It supports Python 2.7, 3.5, 3.6, and pypy.

# Installation

```
$ pip install cannerflow-python-client
```

# Quick Start

## Client
```python
client = cannerflow.client.bootstrap(
    endpoint='http://localhost:3000',
    workspaceId="c6ce7832-ab83-4d7e-bad3-17397b8f6bdb",
    token="token"
)
queries = client.list_saved_query()
cursor = client.use_saved_query('region')
raws = cursor.get_all()
```

## DBAPI
Use the DBAPI interface to query cannerflow:

```python
import cannerflow
conn=cannerflow.dbapi.connect(
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
