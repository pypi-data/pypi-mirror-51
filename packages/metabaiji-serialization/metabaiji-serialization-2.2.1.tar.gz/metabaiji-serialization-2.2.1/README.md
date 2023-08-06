baiji-serialization
===================

[![pip install](https://img.shields.io/badge/pip%20install-metabaiji--serialization-f441b8?style=flat-square)][pypi]
[![version](https://img.shields.io/pypi/v/metabaiji-serialization?style=flat-square)][pypi]
[![python versions](https://img.shields.io/pypi/pyversions/metabaiji-serialization?style=flat-square)][pypi]
[![build status](https://img.shields.io/circleci/project/github/metabolize/baiji-serialization/master?style=flat-square)][circle]
[![last commit](https://img.shields.io/github/last-commit/metabolize/baiji-serialization?style=flat-square)][commits]
[![open pull requests](https://img.shields.io/github/issues-pr/metabolize/baiji-serialization?style=flat-square)][pull requests]

This is an active fork of [baiji-serialization][upstream], a library for
reading and writing common file formats to Amazon S3 and local files.

The fork's goals are modest:

- Keep the library working in current versions of Python and other tools.
- Make bug fixes.
- Provide API stability and backward compatibility with the upstream version.
- Respond to community contributions.

It's used by related forks such as [lace][].

[upstream]: https://github.com/bodylabs/baiji-serialization
[circle]: https://circleci.com/gh/metabolize/baiji-serialization
[pypi]: https://pypi.org/project/metabaiji-serialization/
[pull requests]: https://github.com/metabolize/baiji-serialization/pulls
[commits]: https://github.com/metabolize/baiji-serialization/commits/master
[baiji]: https://github.com/bodylabs/baiji
[lace]: https://github.com/metabolize/lace


Features
--------

- Reads and writes Pickle, JSON, and YAML
- Works without an S3 connection (with local files)
- Supports Python 2.7 and uses boto2
- Supports OS X, Linux, and Windows
- Tested and production-hardened


Examples
--------

```py
from baiji.serialization import json
with open(filename, 'w') as f:
    json.dump(foo, f)
with open(filename, 'r') as f:
    foo = json.load(foo, f)
```

```py
from baiji.serialization import json
json.dump(filename)
foo = json.load(filename)
```


Development
-----------

```sh
pip install -r requirements_dev.txt
rake test
rake lint
```


Contribute
----------

- Issue Tracker: github.com/bodylabs/baiji-serialization/issues
- Source Code: github.com/bodylabs/baiji-serialization

Pull requests welcome!


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the Apache license, version 2.0.
