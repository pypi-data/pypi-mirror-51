.. _api:

===
API
===

.. automodule:: cihai.core
    :members:

Configuration
-------------

.. automodule:: cihai.config
    :members:

Database
--------

.. automodule:: cihai.db
    :members:

Extending
---------

.. automodule:: cihai.extend
    :members:

Constants
---------
.. automodule:: cihai.constants
    :members:

UNIHAN Dataset
--------------

Bootstrapping
~~~~~~~~~~~~~

.. automodule:: cihai.data.unihan.bootstrap
    :members:

.. autoclass:: cihai.data.unihan.dataset.Unihan
   :members:
   :inherited-members:
   :show-inheritance:

.. automodule:: cihai.data.unihan.constants
   :members:
   :inherited-members:
   :show-inheritance:

Variants plugin
~~~~~~~~~~~~~~~

.. autoclass:: cihai.data.unihan.dataset.UnihanVariants
   :members:
   :inherited-members:
   :show-inheritance:

.. _cihai.conversion:

Conversion
----------

.. autofunction:: cihai.conversion.euc_to_unicode
.. autofunction:: cihai.conversion.euc_to_utf8
.. autofunction:: cihai.conversion.gb2312_to_euc
.. autofunction:: cihai.conversion.kuten_to_gb2312
.. autofunction:: cihai.conversion.python_to_euc
.. autofunction:: cihai.conversion.python_to_ucn
.. autofunction:: cihai.conversion.ucn_to_unicode
.. autofunction:: cihai.conversion.ucnstring_to_python
.. autofunction:: cihai.conversion.ucnstring_to_unicode

Exceptions
----------

When using cihai via Python, you can catch Cihai-specific exceptions via
these. All Cihai-specific exceptions are catchable via
:exc:`~cihai.exc.CihaiException` since its the base exception.

.. automodule:: cihai.exc
    :members:
    :inherited-members:
    :show-inheritance:

Utilities
---------

.. automodule:: cihai.utils
    :members:
    :inherited-members:
    :show-inheritance:
