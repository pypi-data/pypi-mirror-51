====
psed
====


CLI utility for text search / replace.

This project is a simple replacement for the ``sed`` in Linux. I had enough issues with
debugging the regular expressions, especially a few months after they were written, so I
have created a replacement in Python. Feel free to use it, but the project aimed to cover
my use case so it might not fit everybody. I plan to improve functionality in the future.

Installation and usage
======================

To install, simply run ``pip install`` command. You need at least Python 3.6 interpreter.

.. code-block::

    pip install psed

Usage:

.. code-block::

    $ psed --help

    Usage: psed [OPTIONS]

      Console script for psed.

    Options:
      -i, --input TEXT    Path to the input file / directory.  [required]
      -f, --find TEXT     String to find.
      -r, --replace TEXT  String to replace.
      --inplace           Modify the file(s) in place.
      -v, --verbose       Increase verbosity.
      --version           Show the version and exit.
      --help              Show this message and exit.



Usage example
=============

Input file:

.. code-block::

    [ERROR] Some error
    [INFO] Some info
    [WARNING] Some warning
    [ERROR] Other error
    [ERROR] There's a lot of errors
    [DEBUG] And one debug

Run psed:

.. code-block::

    psed --input ./sample \
         --find '\[(ERROR)\]' \
         --find '\[(INFO)\]' \
         --find '\[(WARNING)\]' \
         --replace '[LIGHT_\1]'

Output file:

.. code-block::

    [LIGHT_ERROR] Some error
    [LIGHT_INFO] Some info
    [LIGHT_WARNING] Some warning
    [LIGHT_ERROR] Other error
    [LIGHT_ERROR] There's a lot of errors
    [DEBUG] And one debug
