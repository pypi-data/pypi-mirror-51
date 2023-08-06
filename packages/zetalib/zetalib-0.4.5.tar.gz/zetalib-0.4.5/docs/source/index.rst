=================================================================
Zeta -- computing zeta functions of groups, algebras, and modules
=================================================================

Introduction
============

Zeta provides methods for computing local and topological zeta functions
arising from the enumeration of subalgebras, ideals, submodules, and
representations of suitable algebraic structures as well as some other
types of zeta functions. For theoretical background and descriptions of
the methods used, see :ref:`references`.

This package is an *experimental fork* of Zeta, turning it into a
pip-installable SageMath package.

Zeta is distributed as a `Python <http://www.python.org>`_-package for the
computer algebra system `SageMath <http://sagemath.org/>`_. In addition to
`Singular <https://www.singular.uni-kl.de>`_ and other software included with
Sage, Zeta also relies on `LattE integrale
<https://www.math.ucdavis.edu/~latte/software.php>`_ and `Normaliz
<https://www.normaliz.uni-osnabrueck.de>`_.

This work is supported by the `Alexander von
Humboldt-Foundation <https://www.humboldt-foundation.de>`_. From
2013–2016, the development of Zeta was supported by the
`DFG <http://www.dfg.de>`_ Priority Programme "`Algorithmic and
Experimental Methods in Algebra, Geometry and Number
Theory <https://spp.computeralgebra.de>`_".

Please also check the `original homepage of Zeta
<http://www.maths.nuigalway.ie/~rossmann/Zeta/>`_ by `Tobias Rossmann
<http://www.maths.nuigalway.ie/~rossmann/>`_.

Installation
============

Dependencies
------------

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

If you want to use your own versions of these progrmas, you can set the
variables ``zetalib.common.count`` and ``zetalib.common.normaliz`` for the
desired paths, respectively.

Older versions of Zeta required a patched version of ``count``. To that end,
the file ``latte-int-1.7.3/code/latte/genFunction/maple.cpp`` in the sources of
LattE integrale 1.7.3 should be replaced by the file ``maple.cpp`` included
with Zeta. In order to compile the patched version of LattE integrale 1.7.3
from scratch, you may want to use `this modified version
<http://www.maths.nuigalway.ie/~rossmann/Zeta/latte-integrale-1.7.3-for-Zeta.tar>`__
(26M) of the `LattE integrale 1.7.3 bundle
<https://www.math.ucdavis.edu/~latte/software/packages/latte_current/latte-integrale-1.7.3.tar.gz>`__.
Compiled versions of ``normaliz``, ``count`` and ``scdd_gmp`` were included in
the ``bin`` directory for ``linux-x86_64`` until version 0.4.0.

Install from PyPI
-----------------

The easiest way to obtain Zeta is to run::

    $ sage -pip install zetalib

Local install from source
-------------------------

Download the source from the git repository::

    $ git clone https://gitlab.com/mathzeta2/zetalib.git

For convenience this package contains a ``Makefile`` with some often
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

Build documentation
-------------------

The source files of the documentation are located in the ``docs/source``
directory, and are written in Sage's `Sphinx <http://www.sphinx-doc.org>`_
format.

Generate the HTML documentation by running::

    $ cd docs
    $ sage -sh -c "make html"

Or using the shorthand::

    $ make doc

Then open ``docs/build/html/index.html`` in your browser.

Packaging
=========

All packaging setup is internally done through ``setup.py``. To create a
"source package" run::

    $ sage setup.py sdist

To create a binary wheel package run::

    $ sage setup.py bdist_wheel

Or use the shorthand::

    $ make build_wheel

Basic usage
===========

.. _creating-algebra:

Creating algebras
-----------------

By an **algebra**, we mean a free `\mathbf{Z}`-module of finite rank
endowed with a biadditive multiplication; we do not require this
multiplication to be associative or Lie. Given a `\mathbf Z`-basis
`x_1,\dotsc,x_d` of an algebra `L`, define `\alpha_{ije}\in
\mathbf Z` by

.. MATH::

    x_i x_j = \sum_{e=1}^d \alpha_{ije} x_e.

The numbers `\alpha_{ije}` are the **structure constants** of `L` with
respect to the chosen basis `(x_1,\dotsc,x_d)`. The principal method
for specifying an algebra in Zeta is to provide structure constants as a
nested list

.. MATH::

    \begin{matrix}
    [[ (\alpha_{111},\dotsc,\alpha_{11d}), &
    \dotsc & (\alpha_{1d1},\dotsc,\alpha_{1dd}) ]\phantom], \\
    \vdots & & \vdots \\
    \phantom[[ (\alpha_{d11},\dotsc,\alpha_{d1d}), & \dotsc &
    (\alpha_{dd1},\dotsc,\alpha_{ddd}) ]] \\
    \end{matrix}

as the first argument of ``zetalib.Algebra``. (We note that the table of
structure constants of an instance of ``zetalib.Algebra`` is stored in the
``table`` attribute.)

.. _computing-topological-zeta-functions:

Computing topological zeta functions
------------------------------------

Given an algebra obtained via ``zetalib.Algebra``, the function
``zetalib.topological_zeta_function`` can be used to attempt to compute an
associated topological zeta function. Specifically,
``zetalib.topological_zeta_function(L, 'subalgebras')`` will attempt to
compute the topological subalgebra zeta function of `L` as a rational
function in `s`, while ``zetalib.topological_zeta_function(L, 'ideals')``
will do the same for ideals. If `L` is a nilpotent Lie algebra, then
``zetalib.topological_zeta_function(L, 'reps')`` will attempt to compute
the topological representation zeta function of the unipotent algebraic
group over `\mathbf Q` corresponding to `L\otimes_{\mathbf Z}
\mathbf Q`.

In general, such computations are not guaranteed to succeed. If the method for
computing topological zeta functions from [Ro2015a_, Ro2015b_] (for subalgebras
and ideals) or [Ro2016]_ (for representations) fails,
``zetalib.topological_zeta_function`` will raise an exception of type
``zetalib.ReductionError``. Disregarding bugs in Zeta, Sage, or elsewhere,
whenever ``zetalib.topological_zeta_function`` does finish successfully,
its output is supposed to be correct.

.. _example-subalgebras-and-ideals:

Example (subalgebras and ideals)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To illustrate the computation of topological subobject zeta functions,
consider the commutative algebra `L = \mathbf Z[X]/X^3`. As a `\mathbf
Z`-basis of `L`, we choose `(1,x,x^2)`, where `x` is the image of `X` in
`L`. The associated nested list of structure constants is

.. MATH::

    \begin{matrix}
    [[(1, 0, 0), & (0, 1, 0), & (0, 0, 1)]\phantom],\\
    \phantom[ [(0, 1, 0), & (0, 0, 1), & (0, 0, 0)]\phantom],\\
    \phantom[[(0, 0, 1), & (0, 0, 0), & (0, 0, 0)]].
    \end{matrix}

The following documents a complete Sage session leading to the
computation of the topological subalgebra and ideal zeta functions of
`L`.

::

    sage: import zetalib
    sage: L = zetalib.Algebra([[(1, 0, 0), (0, 1, 0), (0, 0, 1)], [(0, 1, 0), (0, 0,1), (0, 0, 0)], [(0, 0, 1), (0, 0, 0), (0, 0, 0)]])
    sage: zetalib.topological_zeta_function(L, 'subalgebras')
    2*(15*s - 8)/((5*s - 4)*(3*s - 2)^2*s)
    sage: zetalib.topological_zeta_function(L, 'ideals')
    1/((3*s - 2)*(2*s - 1)*s)

Example (representations)
^^^^^^^^^^^^^^^^^^^^^^^^^

We illustrate the computation of topological representation zeta
functions of unipotent algebraic groups (over `\mathbf Q`) using the
familiar example of the Heisenberg group `\mathbf H`. The first step is
to construct a `\mathbf Z`-form of its Lie algebra. We choose the
natural `\mathbf Z`-form `L = \mathbf Z x_1 \oplus \mathbf Z x_2
\oplus \mathbf Z x_3` with `[x_1,x_2] = x_3`, `[x_2,x_1] =
-x_3` and `[x_i,x_j] = 0` in the remaining cases. The list of
structure constants of `L` with respect to the basis `(x_1,x_2,x_3)`
is

.. MATH::

    \begin{matrix}
    [[(0, 0, \phantom-0), & (0, 0, 1), & (0, 0, 0)]\phantom],\\
    \phantom[ [(0, 0, -1), & (0, 0, 0), & (0, 0,0)]\phantom],\\
    \phantom[[(0, 0, \phantom-0), & (0, 0, 0), & (0, 0, 0)]].
    \end{matrix}

The following documents a complete Sage session leading to the
computation of the topological representation zeta function of `\mathbf
H`.

::

    sage: import zetalib
    sage: L = zetalib.Algebra([[(0, 0, 0), (0, 0, 1), (0, 0, 0)], [(0, 0,-1), (0, 0, 0), (0, 0, 0)], [(0, 0, 0), (0, 0, 0), (0, 0, 0)]])
    sage: zetalib.topological_zeta_function(L, 'reps')
    s/(s - 1)

.. _computing-local-zeta-functions:

Computing local zeta functions
------------------------------

Uniform zeta functions
^^^^^^^^^^^^^^^^^^^^^^

Using most of the same arguments as ``zetalib.topological_zeta_function`` from
:ref:`computing-topological-zeta-functions`, the function
``zetalib.local_zeta_function`` can be used to attempt to compute *generic*
local subalgebra, ideal, or representation zeta functions—that is to say,
computed zeta functions will be valid for all but finitely many primes `p` and
arbitrary finite extensions of `\mathbf Q_p` as in [Ro2015a_, §5.2] and
[Ro2016_, §2.2]. If the method from [Ro2018a]_ is unable to compute a specific
zeta function, an exception of type ``zetalib.ReductionError`` will be raised.

By default, ``zetalib.local_zeta_function`` will attempt to construct a
single rational function, `W(q,t)` say, in `(q,t)` such that for almost
all primes `p` and all `q = p^f` (`f \ge 1`), the local zeta function
in question obtained after base extension from `\mathbf Q_p` to a
degree `f` extension is given by `W(q,q^{-s})`. Crucially, such a
rational function `W(q,t)` need not exist and even if it does, Zeta may
be unable to compute it.

Example (uniform local zeta functions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let `L` be the Heisenberg Lie algebra as above. The following computes
the associated generic local subalgebra, ideal, and representation zeta
functions.

::

    sage: import zetalib
    sage: L = zetalib.Algebra([[(0, 0, 0), (0, 0, 1), (0, 0, 0)], [(0, 0,-1), (0, 0, 0), (0, 0, 0)], [(0, 0, 0), (0, 0, 0), (0, 0, 0)]])
    sage: zetalib.local_zeta_function(L, 'subalgebras')
    -(q^2*t^2 + q*t + 1)/((q^3*t^2 - 1)*(q*t + 1)*(q*t - 1)*(t - 1))
    sage: zetalib.local_zeta_function(L, 'ideals')
    -1/((q^2*t^3 - 1)*(q*t - 1)*(t - 1))
    sage: zetalib.local_zeta_function(L, 'reps')
    (t - 1)/(q*t - 1)

That is, for almost all primes `p` and all finite extensions `K/\mathbf
Q_p`, the subalgebra and ideal zeta functions of `L \otimes \mathfrak
O_K` are exactly the first two rational functions in `q` and `t =
q^{-s}`; here, `\mathfrak O_K` denotes the valuation ring of `K` and
`q` the residue field size. These results are due to :doi:`Grunewald, Segal,
and Smith <10.1007/BF01393692>` and in fact valid
for arbitrary `p`; the restriction to `K = \mathbf Q_p` in their work
is not essential. Similarly, the above computation using Zeta shows that
if `H \leqslant \mathrm{GL}_3` is the Heisenberg group scheme, then
for almost all primes `p` and all finite extensions `K/\mathbf Q_p`,
the representation zeta function of `H(\mathfrak O_K)` is
`(q^{-s}-1)/(q^{1-s}-1)`, as proved (for all `p`) by :doi:`Stasinski and
Voll <10.1353/ajm.2014.0010>`.

.. _non-uniform-zeta-functions-the-symbolic-mode:

Non-uniform zeta functions: the symbolic mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assuming the method from [Ro2018a]_ applies, Zeta supports
limited computations of non-uniform generic local zeta functions—that
is, instances where no rational function `W(q,t)` as above exists. For
that purpose, ``symbolic=True`` needs to be passed to
``zetalib.local_zeta_function``. If successful, the output will then be
given by a rational function in `q`, `t`, and finitely many variables of
the form ``sc_i``, each corresponding to the number of rational points
over the residue field of `K` of (the reduction modulo `p` of) the
subvariety ``zetalib.common.symbolic_count_varieties[i]`` of some algebraic
torus.

Example (non-uniform local zeta functions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let `L` be the Lie algebra with `\mathbf Z`-basis `(x_1,\dotsc,x_6)` and
non-trivial commutators `[x_1,x_2] = x_3`, `[x_1,x_3] = x_5`, `[x_1,x_4] =
3x_6`, `[x_2,x_3] = x_6`, and `[x_2,x_4] = x_5`; this algebra is called
`L_{6,24}(3)` in :doi:`de Graaf's classification
<10.1016/j.jalgebra.2006.08.006>`. We may compute the generic local
representation zeta functions associated with `L` as follows.

::

    sage: import zetalib
    sage: table = [zero_matrix(6,6) for _ in range(6)]
    sage: table[0][1,2] = 1; table[1][0,2] = -1
    sage: table[0][2,4] = 1; table[2][0,4] = -1
    sage: table[0][3,5] = 3; table[3][0,5] = -3
    sage: table[1][2,5] = 1; table[2][1,5] = -1
    sage: table[1][3,4] = 1; table[3][1,4] = -1
    sage: L = zetalib.Algebra(table)
    sage: zetalib.local_zeta_function(L, 'reps', symbolic=True)
    -(q*sc_0*t - q*t^2 - sc_0*t + 1)*(t - 1)/((q^3*t^2 - 1)*(q*t - 1))
    sage: zetalib.common.symbolic_count_varieties[0]
    Subvariety of 1-dimensional torus defined by [x^2 - 3]

We thus see how the generic local representation zeta functions
associated with `L` depend on whether `3` is a square in the residue
field of `K`. Calling ``zetalib.local_zeta_function(L, 'reps')`` without
``symbolic=True`` will result in an error. As computations with
``symbolic=True`` are generally substantially more computationally
demanding, they should only be attempted as a last resort.

Computing Igusa-type zeta functions
-----------------------------------

Zeta also provides rudimentary support for the computation of local and
topological zeta functions associated with polynomials and polynomial mappings
under the non-degeneracy assumptions from [Ro2015a]_.  Given `f_1,\dotsc,f_r
\in \mathbf Q[X_1,\dotsc,X_n]`, Zeta can be used to attempt to compute the
generic local zeta functions (in the sense discussed above) defined by

.. MATH::

    \int_{\mathfrak O_K^n} \lVert f_1(x),\dotsc, f_r(x) \rVert^s_K \mathrm d\mu_K(x)

or the associated topological zeta function; here, `\mu_K` denotes the Haar
measure and `\lVert \cdotp \rVert_K` the maximum norm, both normalised as
usual.

For a single polynomial, the method used by Zeta is very closely related to
combinatorial formulae of :doi:`Denef and Loeser <10.2307/2152708>` and
:doi:`Denef and Hoornaert <10.1006/jnth.2000.2606>`. In order to attempt to
compute topological or generic local zeta functions associated with a
polynomial (or a polynomial mapping), simply pass a multivariate polynomial (or
a list of these) to ``zetalib.topological_zeta_function`` or
``zetalib.local_zeta_function``, respectively.

Example (Igusa-type zeta functions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following computes the local and topological zeta functions associated with
`f` and `(f,g)`, where `f = X^3 - XYZ` and `g = X^2 - Y^2`.

::

    sage: import zetalib
    sage: R.<x,y,z> = QQ[]
    sage: f = x^3 -x*y*z
    sage: g = x^2 - y^2
    sage: zetalib.local_zeta_function(f)
    (q^4 + q^2*t^2 - q^3 - 2*q^2*t - q*t^2 + q^2 + t^2)*(q - 1)/((q^2 + q*t + t^2)*(q - t)^3)
    sage: zetalib.topological_zeta_function(f)
    1/3*(s^2 + 2*s + 3)/(s + 1)^3
    sage: zetalib.local_zeta_function([f,g])
    (q^2 + 2*q + t)*(q - 1)^2/((q^2 - t)*(q + t)*(q - t))
    sage: zetalib.topological_zeta_function([f,g])
    2/((s + 2)*(s + 1))

Non-uniform examples can be handled as in
:ref:`non-uniform-zeta-functions-the-symbolic-mode`.

Modules and algebras with operators
-----------------------------------

In [Ro2015a_, Ro2015b_], (topological) ideal zeta
functions were treated as special cases of submodule zeta functions. In
Zeta, we regard modules as special cases of algebras with operators.
Namely, each algebra `L` in Zeta is endowed with a possibly empty set
`\Omega` of operators, i.e. `\Omega` consists of additive
endomorphisms of `L`. The topological and local subalgebra and ideal
zeta functions of `L` are always understood to be those arising from the
enumeration of `\Omega`-invariant subalgebras or ideals, respectively.
Thus, if the multiplication of `L` is trivial, then the
`\Omega`-invariant subalgebras (and ideals) of `L` are precisely the
submodules of `L` under the action of the enveloping associative unital
ring of `\Omega` within `\mathrm{End}(L)`.

In practice, `\Omega` is given by a finite list of matrices (or nested
lists of integers representing those matrices) corresponding to the
defining basis of `L`. This list is then supplied to ``zetalib.Algebra``
using the keyword parameter ``operators``. For algebras with zero
multiplication, instead of entering structure constants, you can provide
a keyword argument ``rank`` to ``zetalib.Algebra`` which initialises all
structure constants to zero.

Example (operators)
^^^^^^^^^^^^^^^^^^^

We illustrate the computation of the topological submodule zeta function
arising from the enumeration of sublattices within `\mathbf Z^3`
invariant under the matrix

.. MATH::

    \begin{bmatrix}
    1 & 1 & -1 \\
    0 & 1 & 1 \\
    0 & 0 & 1
    \end{bmatrix}

::

    sage: import zetalib
    sage: M = zetalib.Algebra(rank=3, operators=[ [[1,1,-1],[0,1,1],[0,0,1]] ])
    sage: zetalib.topological_zeta_function(M)
    1/((3*s - 2)*(2*s - 1)*s)

In the database included with Zeta, for examples of algebras with
trivial multiplication but non-empty lists of operators, we did not
include ideal zeta functions; they coincide with the corresponding
subalgebra and submodule zeta functions.

.. _average-sizes-of-kernels:

Average sizes of kernels
------------------------

Subject to the same restrictions as above, Zeta supports the computation of the
(local) "ask zeta functions" defined and studied in [Ro2018b]_.

Let `\mathfrak{O}` be a compact discrete valuation ring with maximal
ideal `\mathfrak{P}`. Let `M \subset \mathrm{M}_{d\times
e}(\mathfrak{O})` be a submodule. Let `M_n \subset
\mathrm{M}_{d\times e}(\mathfrak{O}/\mathfrak{P}^n)` denote the
image of `M` under the natural map `\mathrm{M}_{d\times
e}(\mathfrak{O}) \to \mathrm{M}_{d\times
e}(\mathfrak{O}/\mathfrak{P}^n)`. The **ask zeta function** of `M` is

.. MATH::

    \mathsf{Z}_M(t) = \sum_{n=0}^\infty \mathrm{ask}(M_n) t^n,

where `\mathrm{ask}(M_n)` denotes the average size of the kernels
of the elements of `M_n` acting by right-multiplication on
`(\mathfrak{O}/\mathfrak{P}^n)^d`.

Zeta can be used to attempt to compute generic local ask zeta functions in the
following global setting. Let `M \subset \mathrm{M}_{d\times e}(\mathbf{Z})` be
a submodule of rank `\ell`. Let `A` be an integral `d \times e` matrix of
linear forms in `\ell` variables such that `M` is precisely the module of
specialisations of `A`. Then ``zetalib.local_zeta_function(A, 'ask')``
attempts to compute `\mathsf{Z}_{M \otimes \mathfrak{O}_K}(t)` for almost all
primes `p` and all finite extensions `K/\mathbf{Q}_p` in the same sense as in
:ref:`computing-local-zeta-functions`. The optional keyword parameter ``mode``
determines whether Zeta attempts to compute ask zeta functions using the
functions `\mathrm{K}_M` (``mode='K'``) or `\mathrm{O}_M` (``mode='O'``) from
[Ro2018b_, §4], respectively; the default is ``mode='O'``.


Example (ask zeta function)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

We compute the generic local ask zeta functions associated with
`\mathrm{M}_{2\times 3}(\mathbf{Z})`.

::

    sage: import zetalib
    sage: R.<a,b,c,d,e,f> = QQ[]
    sage: A = matrix([[a,b,c],[d,e,f]])
    sage: zetalib.local_zeta_function(A, 'ask')
    -(q^3 - t)/((q - t)*q^2*(t - 1))

Conjugacy class zeta functions
------------------------------

Let `L` be a nilpotent Lie algebra constructed as in
:ref:`creating-algebra`. Then ``zetalib.local_zeta_function(L, 'cc')``
attempts to compute the generic local conjugacy class zeta functions
associated with the unipotent algebraic group corresponding to `L
\otimes \mathbf{Q}`; see [Ro2018b_, §7.5]. The optional keyword
parameter ``mode`` has the same interpretation as in
:ref:`average-sizes-of-kernels`.

Example
^^^^^^^

We compute the generic local conjugacy class zeta functions of the
Heisenberg group.

::

    sage: import zetalib
    sage: L = zetalib.Algebra([[(0, 0, 0), (0, 0, 1), (0, 0, 0)], [(0, 0,-1), (0, 0, 0), (0, 0, 0)], [(0, 0, 0), (0, 0, 0), (0, 0, 0)]])
    sage: zetalib.local_zeta_function(L, 'cc')
    -(t - 1)/((q^2*t - 1)*(q*t - 1))

.. _the-built-in-database-of-examples:

The built-in database of examples
=================================

Accessing the database
----------------------

Zeta includes a “database” of algebras. When topological or local zeta
functions associated with an algebra in the database have been
successfully computed using Zeta, these are stored as well.

Each algebra stored in Zeta can be referred to using its unique
identification number or one of finitely many names; identification
numbers may change between versions of Zeta. Access to these algebras is
provided using the function ``zetalib.lookup``.

If ``zetalib.lookup`` is called with precisely one argument ``entry``, then
``entry`` should be either an identification number or a name of an
algebra, `L` say, in the database. In this case, ``zetalib.lookup`` will
return `L`. Optional further arguments to ``zetalib.lookup`` can be used to
access other information about `L`:

-  If the second argument is ``'subalgebras'``, ``'ideals'``, or
   ``'reps'`` and the third argument is ``'local'`` or
   ``'topological'``, then ``zetalib.lookup`` will return the local or
   topological subalgebra, ideal, or representation zeta function of
   `L`, respectively, if it is known, and ``None`` otherwise.
-  If the second argument is ``'id'``, then ``zetalib.lookup`` returns the
   identification number of `L`.
-  If the second argument is ``'names'``, then ``zetalib.lookup`` returns a
   list of the stored names of `L`.

When called without arguments, ``zetalib.lookup`` returns a list of pairs
``(i,names)``, where ``i`` ranges over the identification numbers of all
algebras in the database and ``names`` is a possibly empty list of names
associated with the ``i``\ th algebra.

Example
^^^^^^^

The algebra `L = \mathbf Z[X]/X^3` from :ref:`example-subalgebras-and-ideals`
is known to Zeta under the name ``'ZZ[X]/X^3'``; it can be retrieved via ``L =
zetalib.lookup('ZZ[X]/X^3')``. We may recover the pre-computed topological zeta
functions of `L` as follows:

::

    sage: import zetalib
    sage: zetalib.lookup('ZZ[X]/X^3', 'subalgebras', 'topological')
    2*(15*s - 8)/((5*s - 4)*(3*s - 2)^2*s)
    sage: zetalib.lookup('ZZ[X]/X^3', 'ideals', 'topological')
    1/((3*s - 2)*(2*s - 1)*s)

Algebras and their names
------------------------

Apart from self-explanatory names such as ``'sl(2,ZZ)'`` and
``'gl(2,ZZ)'``, Zeta also includes algebras `L_{d,i}`,
`L_{d,i}(\varepsilon)`, `L^i`, `L^i_a`, `M^i`, and `M^i_a` taken
from de Graaf's tables of
:doi:`nilpotent <10.1016/j.jalgebra.2006.08.006>` and
`soluble <http://projecteuclid.org/euclid.em/1120145567>`__ Lie
algebras; their corresponding names in Zeta are of the form
``'L(d,i)'``, ``'L(d,i;eps)'``, ``'L^i'``, ``'L^i(a)'``, ``'M^i'``, and
``'M^i(a)'``. For the infinite families among these algebras, we only
included selected specialisations of the parameters. Recall
[Ro2015a_, Prop. 5.19(ii)] that the topological subalgebra and
ideal zeta functions of an algebra `L` (over `\mathbf Z`) only depend
on the `\mathbf C`-isomorphism type of `L\otimes_{\mathbf Z}\mathbf
C`; a similar statement holds for topological representation zeta
functions by [Ro2016_, Prop. 4.3].

Similar to `Woodward's tables <http://www.lack-of.org.uk/zfarchive/>`__, we use
the notation ``'g(...)'`` to refer to `\mathbf Z`-forms of algebras from
:doi:`Seeley <10.2307/2154390>`'s list of 7-dimensional nilpotent Lie algebras
over `\mathbf C`; for example ``'g(147A)'`` is a `\mathbf Z`-form of the
algebra `1,4,7_A` in Seeley's list.

The algebras ``'N_i^(8,d)'`` are taken from the lists of :doi:`Ren and Zhu
<10.1080/00927872.2010.483342>`, and :doi:`Yan and Deng
<10.1007/s10587-013-0057-6>`.

The algebras called ``'C(d,i)'`` and ``'C(d,i;eps)'`` in Zeta are
“commutative versions” of the nilpotent Lie rings ``'L(d,i)'`` and
``'L(d,i;eps)'`` respectively: they were obtained by inverting the signs
of all entries underneath the diagonal in the matrices of structure
constants.

An algebra called ``'name[eps]'`` in Zeta is obtained by tensoring
``'name'`` with the dual numbers as in [Ro2016_, §6].

Listing algebras, topological zeta functions, and their properties
------------------------------------------------------------------

The function ``zetalib.examples.printall`` generates a text-based list of

-  algebras known to Zeta,
-  structural information about each algebra,
-  known associated topological zeta functions,
-  numerical invariants of these zeta functions (degree, complex roots,
   ...)

and writes these to an optional file-like object (which defaults to
``stdout``). The output of this function is also available for
`download <http://www.math.uni-bielefeld.de/~rossmann/Zeta/topzetas.txt>`__.

By the **essential value** of a rational function `Z\in \mathbf Q(s)`
at a point `w\in \mathbf C`, we mean the value of `Z/(s-w)^m` at `s =
w`, where `m` is the order of `Z` at `w`; similarly, for `w = \infty`.
The output of ``zetalib.examples.printall`` (and hence the content of the
file linked to above) contains the essential values of topological zeta
functions at `0` and `\infty`; these are related to Conjectures IV–V
from [Ro2015a_, Ro2015b_].

Advanced usage
==============

More on the creation of algebras
--------------------------------

As an integral version of terminology used by
:doi:`Evseev <10.1515/CRELLE.2009.065>`, we say that a
`\mathbf Z`-basis `(x_1,\dotsc,x_d)` of an algebra `L` is **simple**
if each product `x_ix_j` is of the form `\varepsilon_{ij}
x_{a_{ij}}` for `\varepsilon_{ij} \in \{-1,0,1\}`. In this case,
the structure constants of `L` with respect to `(x_1,\dotsc,x_d)` are
determined by the matrix `A = [\varepsilon_{ij}
a_{ij}]_{i,j=1,\dotsc,d}`. Zeta supports the creation of algebras
from such a matrix `A` by passing ``simple_basis=True`` and
``matrix=``\ `A` as arguments to ``zetalib.Algebra``.

For example, the Heisenberg Lie ring with `\mathbf Z`-basis `(x_1,x_2,x_3)` and
non-trivial products `[x_1,x_2] = x_3` and `[x_2,x_1] = -x_3` from above can be
defined in Zeta via ``zetalib.Algebra(simple_basis=True, matrix=[[0,3,0],
[-3,0,0], [0,0,0] ])``.

TODO: Add documentation of the ``bilinear`` argument.

Additive gradings: blocks
-------------------------

Zeta supports the computation of graded subalgebra and ideal zeta
functions as in [Ro2018a]_. These zeta functions enumerate
homogeneous subobjects with respect to a given additive decomposition of
the underlying module. Such decompositions are specified using the
keyword argument ``blocks`` of ``zetalib.Algebra``. To that end, ``blocks``
should be assigned a list `(\beta_1,\dotsc,\beta_r)` of positive
integers summing up to the rank of the algebra `L` in question. If
`(x_1,\dotsc,x_d)` is the defining basis of `L`, then the associated
additive decomposition is `L = L_1 \oplus \dotsb \oplus L_r` for
`L_j = \bigoplus_{i=\sigma_{j-1}+1}^{\sigma_j} \mathbf Z x_i`
and `\sigma_i = \sum_{e=1}^i \beta_e`.

Example (graded zeta functions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let `L` be the Heisenberg Lie algebra with `\mathbf Z`-basis
`(x_1,x_2,x_3)` and `[x_1,x_2] = x_3` as above. Then `L = L_1
\oplus L_2` with `L_1 = \mathbf Z x_1 \oplus \mathbf Z x_2` and
`L_2 = \mathbf Z x_3` is the associated graded Lie algebra and the
following computes the generic graded local zeta functions arising from
the enumeration of its homogeneous subalgebras.

::

    sage: import zetalib
    sage: L = zetalib.Algebra([[(0, 0, 0), (0, 0, 1), (0, 0, 0)], [(0, 0,-1), (0, 0, 0), (0, 0, 0)], [(0, 0, 0), (0, 0, 0), (0, 0, 0)]], blocks=[2,1])
    sage: zetalib.local_zeta_function(L, 'subalgebras')
    -(q*t^3 - 1)/((q*t^2 - 1)*(q*t - 1)*(t + 1)*(t - 1)^2)

Changing bases
--------------

(The following only applies to the computation of subalgebra and ideal
zeta functions and not to representation or Igusa-type zeta functions.)
Computations using Zeta are usually very sensitive to the choice of the
basis used to define the structure constants of the algebra under
consideration. If a particular zeta function cannot be directly computed
using Zeta, it might be useful to consider different bases. Given an
algebra ``L`` of rank `d` and an invertible `d\times d` matrix ``A``
over `\mathbf Z`, the algebra obtained from `L` by taking the rows of
``A`` as a basis (relative to the original one) can be constructed via
``L.change_basis(A)``. In the presence of a non-trivial grading, the
latter is required to be respected by ``A``.

Unless ``zetalib.local_zeta_function`` or
``zetalib.topological_zeta_function`` is called with the keyword argument
``optimise_basis=False``, Zeta will attempt to find a basis of the
algebra, `L` say, in question such that the associated toric datum (see
[Ro2015b]_) is “small”. Currently, Zeta simply loops over
permutations of the defining basis of `L`.

Verbosity
---------

If ``zetalib.local_zeta_function`` or ``zetalib.topological_zeta_function`` is
called with the keyword argument ``verbose=True``, then detailed
information on the various stages of computations will be displayed.
Apart from illustrating the key steps explained in
[Ro2015a_, Ro2015b_, Ro2016_, Ro2018a_],
this can often be helpful when it comes to estimating the feasibility of
the intended computation.

Computational resources
-----------------------

An upper bound on the number of CPUs used by
``zetalib.local_zeta_function`` and ``zetalib.topological_zeta_function`` can
be enforced by providing a numerical value for the keyword parameter
``ncpus``.

During computations of zeta functions, Zeta uses various temporary
files. Be warned that for some computations carried out by the author,
the combined size of these files exceeded 50G.

Zeta can be equally demanding when it comes to system memory, in
particular when computing local zeta functions. If computations run out
of memory, you can try reducing the number of CPUs used as indicated
above or try setting the keyword parameter ``profile`` to
``zetalib.Profile.SAVE_MEMORY``. Setting ``profile=zetalib.Profile.SPEED``
will result in slightly better performance at the cost of increased
memory use.

Reduction strategies
--------------------

(The following only applies to the computation of subalgebra and ideal zeta
functions.) The reduction step explained in [Ro2015b]_ depends on a strategy
for choosing “reduction candidates”. A particular strategy can be chosen using
the keyword parameter ``strategy`` of ``zetalib.local_zeta_function`` or
``zetalib.topological_zeta_function``. In particular, setting
``strategy=zetalib.Strategy.NONE`` disables reduction completely while
``strategy=zetalib.Strategy.NORMAL`` yields the strategy used in the paper.
Passing ``strategy=zetalib.Strategy.PREEMPTIVE`` will result in a more
aggressive reduction strategy which tries to anticipate and remove causes of
singularity in advance. While often slower than the
``zetalib.Strategy.NORMAL``, this strategy is needed to reproduce some of the
computations recorded in the database
(:ref:`the-built-in-database-of-examples`).

Acknowledgements
================

* The `Sage Sample Package <https://github.com/sagemath/sage_sample>`_ was used
  as the initial package structure.

.. _references:

References
==========

.. [Ro2015a] T. Rossmann, *Computing topological zeta functions of groups,
    algebras, and modules, I*, Proc. Lond. Math. Soc. (3) 110 (2015), no. 5,
    1099--1134. :doi:`10.1112/plms/pdv012`, `preprint
    <http://www.maths.nuigalway.ie/~rossmann/files/topzeta.pdf>`__.

.. [Ro2015b] T. Rossmann, *Computing topological zeta functions of groups,
    algebras, and modules, II*, J. Algebra 444 (2015), 567--605.
    :doi:`10.1016/j.jalgebra.2015.07.039`, `preprint
    <http://www.maths.nuigalway.ie/~rossmann/files/topzeta2.pdf>`__.

.. [Ro2016] T. Rossmann, *Topological representation zeta functions of
    unipotent groups*, J. Algebra 448 (2016), 210--237.
    :doi:`10.1016/j.jalgebra.2015.09.050`, `preprint
    <http://www.maths.nuigalway.ie/~rossmann/files/unipotent.pdf>`__.

.. [Ro2018a] T. Rossmann, *Computing local zeta functions of groups, algebras,
    and modules*. `preprint
    <http://www.maths.nuigalway.ie/~rossmann/files/padzeta.pdf>`__.

.. [Ro2018b] T. Rossmann, *The average size of the kernel of a matrix and
    orbits of linear groups*. `preprint
    <http://www.maths.nuigalway.ie/~rossmann/files/ask.pdf>`__.

License
=======

See the ``LICENSE`` file. This fork of Zeta is released under
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

.. This built documentation is licensed under a `Creative Commons Attribution-Share Alike 4.0 License <https://creativecommons.org/licenses/by-sa/4.0/>`_.

Individual modules documentation
================================

.. toctree::
    :maxdepth: 1

    algebra
    tmplist

.. toctree::
    :maxdepth: 1
    :hidden:

    todo

There is also a :doc:`todo` list. Contributions are welcomed!

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
