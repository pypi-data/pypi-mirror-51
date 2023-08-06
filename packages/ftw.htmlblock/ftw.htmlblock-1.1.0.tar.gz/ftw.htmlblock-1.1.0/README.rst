.. contents:: Table of Contents


Introduction
============

This package is an addon for `ftw.simplelayout <http://github.com/4teamwork/ftw.simplelayout>`_. Please make sure you
already installed ``ftw.simplelayout`` on your plone site before installing this addon.

HTML blocks allow you to add arbitrary, unfiltered HTML to a content page.

The HTML is not escaped when rendered on the content page so you need to be
especially careful what you do. By default only users having the role
"Manager" are allowed to add HTML blocks.


Installation
============

- Add the package to your buildout configuration:

::

    [instance]
    eggs +=
        ...
        ftw.htmlblock


Usage
=====

Drag a HTML block form the toolbox into your page and fill the textarea.


Development
===========

**Python:**

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buildout.cfg``
4. Shell: ``python boostrap.py``
5. Shell: ``bin/buildout``

Run ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.


Links
=====

- GitHub: https://github.com/4teamwork/ftw.htmlblock
- Issues: https://github.com/4teamwork/ftw.htmlblock/issues
- PyPI: http://pypi.python.org/pypi/ftw.htmlblock
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.htmlblock


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.htmlblock`` is licensed under GNU General Public License, version 2.
