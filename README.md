## Documentation

The documentation of this project may be built with Sphinx.

### How to build it

Commands to build the docs:
```sh
$ python bootstrap.py
$ ./bin/buildout
$ ./bin/docs
````
To set language or manage some other stuff, edit `docs/source/conf.py`

To update files data for tutorial:
```sh
DOCSTEST=True ./bin/nosetests openprocurement.auctions.geb.tests.cases.docs
```