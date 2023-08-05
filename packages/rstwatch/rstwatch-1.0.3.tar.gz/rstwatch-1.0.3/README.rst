========
rstwatch
========
------------------------------------------------------------
Watch directories for changes to RST files and generate HTML
------------------------------------------------------------

:Author: David Handy <cpif@handysoftware.com>

This simple static website generator scans directories for .rst files (text
files in reStructuredText_ format) and converts them to HTML documents using
docutils_.  By default it runs continuously.  Whenever an .rst file (or a
file included by an .rst file) is added or changed, the associated .html
file is immediately created or re-generated.

.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _docutils: http://docutils.sourceforge.net/index.html

Example
=======

- In your web content directory run: ``rstwatch .``
- Create an .rst file in that directory, e.g. named ``index.rst``
- *Immediately a file named* ``index.html`` *appears in that same directory*
- Point your web browser to the ``index.html`` file
- In your editor window, make a change to ``index.rst`` and save it
- In your browser window, hit the refresh button
- **Boom!** *You see your changes, converted to HTML, right away*
- When you are done, press ``Ctrl-C`` to stop ``rstwatch``

You can use ``rstwatch`` to learn and experiment with docutils_ and the
reStructuredText_ format. This can be a stepping-stone to using a more
complicated, fully-featured document generation system based on docutils,
such as Sphinx_.

.. _Sphinx: http://www.sphinx-doc.org/en/stable/index.html

Installation Instructions
=========================

``rstwatch`` is an `open source`_ program written in the Python_ programming
language. (See the `license <LICENSE.txt>`_.)

First, install Python if you haven't already. It is freely available for
Windows_, MacOS_, and Linux (it is likely already installed on MacOS or
Linux.)

Next, install ``rstwatch`` from the `Python Package Index`_ using the pip_
command::

    pip install rstwatch

The source code is hosted at: https://sourceforge.net/projects/rstwatch/

.. _`open source`: https://opensource.org/
.. _Python: https://www.python.org/
.. _Windows: https://www.python.org/downloads/windows/
.. _MacOS: https://www.python.org/downloads/mac-osx/
.. _`Python Package Index`: https://pypi.python.org/pypi
.. _pip: https://pip.pypa.io/en/stable/

Usage
=====

::

    rstwatch [options] <directory>...

Options:

--exit                  Exit after first pass, instead of repeat scanning
--interval=SECONDS      Seconds to delay between directory scans [default: 2.0]
--log-config=FILENAME   (Optional) Custom logging configuration file
--refresh               Regenerate all html files on first scan
--writer=WRITER_NAME    Docutils writer name. [default: html5]

For the (optional) log configuration file format, see:
https://docs.python.org/3/library/logging.config.html#configuration-file-format

Example log config file: `log-config.ini <example/log-config.ini>`__

Related Links
=============

- `rstwatch on bitbucket
  <https://bitbucket.org/dhandy2013/rstwatch/overview>`__
- `reStructuredText quick reference
  <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`__
- `List of built-in reStructuredText directives
  <http://docutils.sourceforge.net/docs/ref/rst/directives.html>`__
