=================================================================
Zeta -- computing zeta functions of groups, algebras, and modules
=================================================================

::

    
    ZZZZZZZZZZZZZZZZZZZ                           tttt                           
    Z:::::::::::::::::Z                        ttt:::t                           
    Z:::::::::::::::::Z                        t:::::t                           
    Z:::ZZZZZZZZ:::::Z                         t:::::t                           
    ZZZZZ     Z:::::Z     eeeeeeeeeeee   ttttttt:::::ttttttt     aaaaaaaaaaaaa   
            Z:::::Z     ee::::::::::::ee t:::::::::::::::::t     a::::::::::::a  
           Z:::::Z     e::::::eeeee:::::et:::::::::::::::::t     aaaaaaaaa:::::a 
          Z:::::Z     e::::::e     e:::::tttttt:::::::tttttt              a::::a 
         Z:::::Z      e:::::::eeeee::::::e     t:::::t             aaaaaaa:::::a 
        Z:::::Z       e:::::::::::::::::e      t:::::t           aa::::::::::::a 
       Z:::::Z        e::::::eeeeeeeeeee       t:::::t          a::::aaaa::::::a 
    ZZZ:::::Z     ZZZZe:::::::e                t:::::t    ttttta::::a    a:::::a 
    Z::::::ZZZZZZZZ:::e::::::::e               t::::::tttt:::::a::::a    a:::::a 
    Z:::::::::::::::::Ze::::::::eeeeeeee       tt::::::::::::::a:::::aaaa::::::a 
    Z:::::::::::::::::Z ee:::::::::::::e         tt:::::::::::tta::::::::::aa:::a
    ZZZZZZZZZZZZZZZZZZZ   eeeeeeeeeeeeee           ttttttttttt   aaaaaaaaaa  aaaa
    
Introduction
------------

Zeta provides methods for computing local and topological zeta functions
arising from the enumeration of subalgebras, ideals, submodules, and
representations of suitable algebraic structures as well as some other types of
zeta functions.

This package is an *experimental fork* of Zeta, turning it into a
pip-installable SageMath package. You can check this `temporary link
<http://u.math.biu.ac.il/~bauerto/zetalib/html/index.html>`_ for the full
documentation.

Please also check the `original homepage of Zeta
<http://www.maths.nuigalway.ie/~rossmann/Zeta/>`_ by `Tobias Rossmann
<http://www.maths.nuigalway.ie/~rossmann/>`_.

Installation
------------

Dependencies
^^^^^^^^^^^^

We assume SageMath version 8.3, or higher, is used.

The `wheel <https://pypi.org/project/wheel/>`__ packaging standard is needed at
installation time. It can be installed by running::

    $ sage -pip install wheel

Zeta will try to invoke the programs ``count`` (a part of `LattE integrale
<https://www.math.ucdavis.edu/~latte/software.php>`__) and ``normaliz`` (a part
of `Normaliz <https://www.normaliz.uni-osnabrueck.de>`__).  They can be
installed by running::

    $ sage -i latte_int
    $ sage -i normaliz

See the full documentation how to use other versions of these programs.

Install from PyPI
^^^^^^^^^^^^^^^^^

The easiest way to obtain Zeta is to run::

    $ sage -pip install zetalib

Local install from source
^^^^^^^^^^^^^^^^^^^^^^^^^

Download the source from the git repository::

    $ git clone https://gitlab.com/mathzeta2/zetalib.git

For convenience this package contains a `Makefile <Makefile>`_ with some often
used commands. To build the C extensions, install and test you should change to
the root directory and run::

    $ make

Alternatively, you can do it in separate steps::

    $ make build
    $ make test
    $ sage -pip install --upgrade --no-index -v . # or `make install`

To uninstall you can run::

    $ sage -pip uninstall zetalib # or `make uninstall`

If you want to use another version of SageMath you have installed, you can
modify the ``SAGE`` variable when calling ``make``::

    $ make SAGE=/path/to/sage build

Usage
-----

Once the package is installed, you can use it in Sage with::

    sage: import zetalib
    sage: M = zetalib.Algebra(rank=3, operators=[ [[1,1,-1], [0,1,1], [0,0,1]] ])
    sage: zetalib.topological_zeta_function(M)
    1/((3*s - 2)*(2*s - 1)*s)

See the documentation for further details.

Packaging
---------

All packaging setup is internally done through `setup.py <setup.py>`_. To
create a "source package" run::

    $ sage setup.py sdist

To create a binary wheel package run::

    $ sage setup.py bdist_wheel

Or use the shorthand::

    $ make build_wheel

Documentation
-------------

The source files of the documentation are located in the `docs/source
<docs/source>`_ directory, and are written in Sage's `Sphinx
<http://www.sphinx-doc.org>`_ format.

Generate the HTML documentation by running::

    $ cd docs
    $ sage -sh -c "make html"

Or using the shorthand::

    $ make doc

Then open ``docs/build/html/index.html`` in your browser.

Acknowledgements
----------------

* The `Sage Sample Package <https://github.com/sagemath/sage_sample>`_ was used
  for the initial package structure.

License
-------

See the `LICENSE <LICENSE>`_ file. This fork of Zeta is released under
GPL-3.0-or-later, like the original version, as quoted in the original
documentation:

    Copyright 2014, 2015, 2016, 2017 Tobias Rossmann.

    Zeta is free software: you can redistribute it and/or modify it under the
    terms of the `GNU General Public License
    <http://www.gnu.org/copyleft/gpl.html>`_ as published by the Free Software
    Foundation, either version 3 of the License, or (at your option) any later
    version.

    Zeta is distributed in the hope that it will be useful, but without
    any warranty; without even the implied warranty of merchantability or
    fitness for a particular purpose. See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with Zeta. If not, see http://www.gnu.org/licenses.
