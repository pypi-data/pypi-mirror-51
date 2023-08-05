Changelog
================

0.2.0 (2018-10-08)
------------------

Features added
~~~~~~~~~~~~~~

* Complete rewrite of the original C-Snake


0.2.1 (2018-10-08)
------------------

Features added
~~~~~~~~~~~~~~

* Tested the CI pipeline for automatic PyPI upload


0.2.2 (2018-10-08)
------------------

Bug fixes
~~~~~~~~~

* Fixed erroneous documentation and PyPI info


0.2.3 (2018-10-08)
------------------

Bug fixes
~~~~~~~~~

* Fixed malformed RST on PyPI

0.2.4 (2018-10-29)
------------------

Features added
~~~~~~~~~~~~~~

* Added support for initialization of Values to PIL (pillow) Images through the
  `pil_image_to_list` utility in the optional `csnake.pil_converter` submodule.
* Enabled Pip package caching for CI
* Improved docstrings of some non-public functions
* Reformatted the Sphinx documentation somewhat.

Bug fixes
~~~~~~~~~

* Fixed several things in tests that produced warnings while testing.
* Fixed escape sequences in RST docstrings.

0.2.5 (2019-08-16)
------------------

* Updated dependencies.

Bug fixes
~~~~~~~~~

* Fixed `Variable.__str__` to work even when `Variable.value` is `None`.
* Fixed several benign things in tests that produced warnings.

0.3.0 (2019-08-20)
------------------

Features added
~~~~~~~~~~~~~~
* `CodeWriterLite.add_lines` and functions using it (like `Function.add_code`) 
  are now able to handle iterators that iterate over multi-line strings, not
  just single-line ones.
* Exposed `CodeWriterLite`.
* Exposed useful Exceptions.
* Refactored CI pipeline, switched Pipenv → Poetry as the packaging tool for
  development dependencies.
