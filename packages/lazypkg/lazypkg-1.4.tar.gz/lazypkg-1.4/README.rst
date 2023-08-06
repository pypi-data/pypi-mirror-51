============================================
lazypkg: lazy import modules and subpackages
============================================

.. image:: http://img.shields.io/pypi/v/lazypkg.svg?style=flat
   :target: https://pypi.python.org/pypi/lazypkg
   :alt: Version_status
.. image:: http://img.shields.io/badge/license-MIT-blue.svg?style=flat
   :target: https://github.com/yoelcortes/lazypkg/blob/master/LICENSE.txt
   :alt: license

.. contents::

What is lazypkg?
----------------

lazypkg features the LazyPkg object, a ModuleType object that lazy imports subpackages and allows access to subpackage objects. Lazy importing is when a submodule is not imported along with the top level module, but is still accessible on demand.

Installation
------------

Get the latest version of lazypkg from
https://pypi.python.org/pypi/lazypkg/

If you have an installation of Python with pip, simple install it with:

    $ pip install lazypkg

To get the git version, run:

    $ git clone git://github.com/yoelcortes/lazypkg

Getting started
---------------

LazyPkg objects are straight forward. First assume the following package structure:

::

  package/
    __init__.py
    module.py
    ...
    subpackage/
      __init__.py
      submodule.py
      ...
   
Here is an example implementation of a LazyPkg object in the package __init__.py file:
     
.. code-block:: python
   
   from lazypkg import LazyPkg
   from .module import obj
   __all__ = ['obj']
   LazyPkg(__name__, ['subpackage'])
   # This converts the package into a LazyPkg object and lazy imports 'subpackage'   

Say the subpackage __init__.py file looks like this:
  
.. code-block:: python
   
   from . import submodule
   __all__ = ['submodule']
   print('imported subpackage')   

When the subpackage is accessed, only then will it be imported:

.. code-block:: python
   
   >>> import package # Subpackages are not imported
   >>> package.obj
   # -> Works just like an ordinary package
   >>> package.subpackage
   imported subpackage
   
Additionally, subpackage object are directly accessible:
   
.. code-block:: python
   
   >>> import package
   >>> package.submodule
   # -> Assuming "submodule" is not defined in the top level package,
   #    this will import and search subpackages for the "submodule"

This is all possible because the package become a LazyPkg instance:

.. code-block:: python
   
   >>> import package
   >>> type(package)
   lazypkg.LazyPkg

Bug reports
-----------

To report bugs, please use the lazypkg's Bug Tracker at:

    https://github.com/yoelcortes/lazypkg


License information
-------------------

See ``LICENSE.txt`` for information on the terms & conditions for usage
of this software, and a DISCLAIMER OF ALL WARRANTIES.

Although not required by the lazypkg license, if it is convenient for you,
please cite lazypkg if used in your work. Please also consider contributing
any changes you make back, and benefit the community.

Citation
--------

To cite lazypkg in publications use::

    Yoel Cortes-Pena. lazypkg: lazy import modules and subpackages.
    https://github.com/yoelcortes/lazypkg
