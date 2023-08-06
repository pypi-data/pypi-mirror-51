Intercessions
=============

|Known Vulnerabilities|\ |Requirements Status|

A blessings polyfill for the windows command line

Attempts to implement the full
`blessings <https://pypi.python.org/pypi/blessings/>`__ API in a format
that will work on windows. Makes use of
`colorama <https://pypi.python.org/pypi/colorama>`__ to help with
styling.

Installation
============

``pip install intercessions``

Usage
=====

.. code:: python

   from intercessions import Terminal

   t = Terminal()
   with t.location(0,0), t.hidden_cursor():
       print(t.bold_red('Hello World!') + t.clear_eol)
       raw_input('Press Enter' + t.clear_eol)

If `blessings <https://pypi.python.org/pypi/blessings/>`__ is installed
and you are not running the windows version of python it will attempt to
return the `blessings <https://pypi.python.org/pypi/blessings/>`__
instance of Terminal instead of the intercessions one.

.. |Known Vulnerabilities| image:: https://snyk.io/test/github/eeems/intercessions/badge.svg
   :target: https://snyk.io/test/github/eeems/intercessions
.. |Requirements Status| image:: https://requires.io/github/Eeems/intercessions/requirements.svg?branch=master
   :target: https://requires.io/github/Eeems/intercessions/requirements/?branch=master

