soph.py
=======

-----

.. contents:: **Table of Contents**
    :backlinks: none

Installation
------------

soph.py is distributed on `PyPI <https://pypi.org>`_ as a universal
wheel and is available on Linux/macOS and Windows and supports
Python 2.7/3.5+ and PyPy.

.. code-block:: bash

    $ pip install soph

Development
-----------

See https://packaging.python.org/tutorials/packaging-projects/ for more info on packaging projects.

For this package, the following code is used to upload changes. This is mostly so I don't forget!

version bump with
```bash
hatch grow major/minor/fix
```

build with
```bash
python3 setup.py sdist bdist_wheel
```

upload with
```bash
hatch release
```

License
-------

soph.py is distributed under the terms of the
`MIT License <https://choosealicense.com/licenses/mit>`_.
