# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pdocs']

package_data = \
{'': ['*'], 'pdocs': ['templates/*']}

install_requires = \
['Mako>=1.1,<2.0', 'Markdown>=3.0.0,<4.0.0', 'hug>=2.6,<3.0']

setup_kwargs = {
    'name': 'pdocs',
    'version': '0.1.3',
    'description': 'A simple program and library to auto generate API documentation for Python modules.',
    'long_description': "\n[![Build Status](https://travis-ci.org/mitmproxy/pdocs.svg?branch=master)](https://travis-ci.org/mitmproxy/pdocs)\n[![PyPI Version](https://shields.mitmproxy.org/pypi/v/pdocs.svg)](https://pypi.org/project/pdocs/)\n\n`pdocs` is a library and a command line program to discover the public\ninterface of a Python module or package. The `pdocs` script can be used to\ngenerate plain text or HTML of a module's public interface, or it can be used\nto run an HTTP server that serves generated HTML for installed modules.\n\n\nInstallation\n------------\n\n    pip install pdocs\n\n\nFeatures\n--------\n\n* Support for documenting data representation by traversing the abstract syntax\n  to find docstrings for module, class and instance variables.\n* For cases where docstrings aren't appropriate (like a\n  [namedtuple](http://docs.python.org/2.7/library/collections.html#namedtuple-factory-function-for-tuples-with-named-fields)),\n  the special variable `__pdocs__` can be used in your module to\n  document any identifier in your public interface.\n* Usage is simple. Just write your documentation as Markdown. There are no\n  added special syntax rules.\n* `pdocs` respects your `__all__` variable when present.\n* `pdocs` will automatically link identifiers in your docstrings to its\n  corresponding documentation.\n* When `pdocs` is run as an HTTP server, external linking is supported between\n  packages.\n* The `pdocs` HTTP server will cache generated documentation and automatically\n  regenerate it if the source code has been updated.\n* When available, source code for modules, functions and classes can be viewed\n  in the HTML documentation.\n* Inheritance is used when possible to infer docstrings for class members.\n\nThe above features are explained in more detail in pdocs's documentation.\n\n`pdocs` is compatible with Python 3.5 and newer.\n\n\nExample usage\n-------------\n`pdocs` will accept a Python module file, package directory or an import path.\nFor example, to view the documentation for the `csv` module in the console:\n\n    pdocs csv\n\nOr, you could view it by pointing at the file directly:\n\n    pdocs /usr/lib/python3.7/csv.py\n\nSubmodules are fine too:\n\n    pdocs multiprocessing.pool\n\nYou can also filter the documentation with a keyword:\n\n    pdocs csv reader\n\nGenerate HTML with the `--html` switch:\n\n    pdocs --html csv\n\nA file called `csv.m.html` will be written to the current directory.\n\nOr start an HTTP server that shows documentation for any installed module:\n\n    pdocs --http\n\nThen open your web browser to `http://localhost:8080`.\n\nThere are many other options to explore. You can see them all by running:\n\n    pdocs --help\n\n\nSubmodule loading\n-----------------\n\n`pdocs` uses idiomatic Python when loading your modules. Therefore, for `pdocs` to\nfind any submodules of the input module you specify on the command line, those\nmodules must be available through Python's ordinary module loading process.\n\nThis is not a problem for globally installed modules like `sys`, but can be a\nproblem for your own sub-modules depending on how you have installed them.\n\nTo ensure that `pdocs` can load any submodules imported by the modules you are\ngenerating documentation for, you should add the appropriate directories to your\n`PYTHONPATH` environment variable.\n\nFor example, if a local module `a.py` imports `b.py` that is installed as\n`/home/jsmith/pylib/b.py`, then you should make sure that your `PYTHONPATH`\nincludes `/home/jsmith/pylib`.\n\nIf `pdocs` cannot load any modules imported by the input module, it will exit\nwith an error message indicating which module could not be loaded.\n",
    'author': 'Timothy Crosley',
    'author_email': 'timothy.crosley@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
