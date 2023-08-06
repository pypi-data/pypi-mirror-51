How to build the documentation
==============================

Install ``virtualenv`` if you don't have it yet:

::

    pip3 install virtualenvwrapper

Create a new ``virtualenv`` and activate it:

::

    virtualenv -p python3 coala-venv
    source coala-venv/bin/activate

You can test the documentation locally through simply running

::

    make html

in the root directory. This generates ``_build/html/index.html`` that you can
view on your browser.

If you want to add new pages, you need to alter the index.rst file in the root
directory. Please read
http://www.sphinx-doc.org/en/stable/markup/toctree.html#toctree-directive for
an explanation of the syntax.