venv-clean
----------

Tool that finds python virtual environments in your machine, displaying interesting data, such as disk usage and packages installed.
It gives the user the chance to delete one or more virtual environments to free disk space.


Usage
-----

.. image:: demos/cli-demo.gif


The package can be used directly on your terminal. The only argument it receives (for now) is the path where you want to look for virtual environments.

.. code-block:: sh

    $ venv-clean -h
    usage: venv_clean [-h] [-p PATH]

    Python Virtual Environment finder & manager

    optional arguments:
      -h, --help            show this help message and exit
      -p PATH, --path PATH  path where to look for virtual environments


Through a TUI, the user will be displayed with the data.


Installation
------------

Latest release through PyPI:

.. code-block:: sh

    $ pip install venv_clean

Development version:

.. code-block:: sh

    $ git clone git@github.com:jcapona/venv-clean.git
    $ cd pi-gpio-api
    $ pip install -e .


Contribute
----------

Feel free to open issues, report bugs or open pull requests.