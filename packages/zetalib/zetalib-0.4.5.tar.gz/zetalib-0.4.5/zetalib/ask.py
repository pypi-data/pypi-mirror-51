from __future__ import absolute_import
from sage.all import *

from . import common

from .util import create_logger, cached_simple_method
from six.moves import range

logger = create_logger(__name__)

from .reps import IgusaDatum, RepresentationProcessor
from .convex import PositiveOrthant, StrictlyPositiveOrthant, RationalSet
from .util import evaluate_matrix
from .laurent import LaurentIdeal, LaurentPolynomial
from .torus import SubvarietyOfTorus
from .abstract import LocalZetaProcessor

class AskProcessor(RepresentationProcessor):
    def __init__(self, arg, mode=None):
        if mode is None:
            mode = 'O'

        if mode not in ['O', 'K']:
            raise ValueError("supported modes are 'O' and 'K'")
        
        self.R = arg
        self.d = self.R.nrows()
        self.e = self.R.ncols()
        self.mode = mode

        self.ring = self.R.base_ring()
        self.ell = self.ring.ngens()

        self.basis = [evaluate_matrix(self.R, y) for y in identity_matrix(QQ, self.ell)]
        V = (QQ**(self.d * self.e)).subspace([A.list() for A in self.basis])
        if V.dimension() != self.ell:
            raise ValueError('subspace parameterised by matrix of linear forms has wrong dimension')

    def padically_evaluate_regular(self, datum):
        # The essential change from representation zeta functions is that
        # the extra variable may be a unit here.
        for z in super(AskProcessor, self).padically_evaluate_regular(datum, extra_RS=RationalSet(PositiveOrthant(1))):
            yield z

    def topologically_evaluate_regular(self, datum):
        raise NotImplementedError

    @cached_simple_method
    def root(self):
        if self.mode == 'K':
            ell = self.ell
            self.RS = RationalSet([PositiveOrthant(ell)], ambient_dim=ell)

            actual_ring = self.ring
            F = FractionField(actual_ring)
            r = matrix(F, self.R).rank()
            self.r = r
            if not self.d:
                return

            F = [
                LaurentIdeal(
                    gens = [LaurentPolynomial(f) for f in self.R.minors(j)],
                    RS = self.RS,
                    normalise = True)
                for j in range(r+1)
            ]
        elif self.mode == 'O':
            self.RS = RationalSet([PositiveOrthant(self.d)], ambient_dim=self.d)
            actual_ring = PolynomialRing(QQ, 'x', self.d)
            xx = vector(actual_ring, actual_ring.gens())
            self.C = matrix(actual_ring, [xx * matrix(actual_ring,A) for A in self.basis])
            r = matrix(FractionField(actual_ring), self.C).rank()
            self.r = r
            if not self.d:
                return
            F = [
                LaurentIdeal(
                    gens = [LaurentPolynomial(f) for f in self.C.minors(j)],
                    RS = self.RS,
                    normalise = True)
                for j in range(r+1)
            ]
        else:
            raise ValueError('invalid mode')

        oo = r + 1

        # On pairs:
        # The first component is used as is, the second is multiplied by the extra
        # variable. Note that index 0 corresponds to {1} and index oo to {0}.
        self.pairs = (
            [(oo,0)] +
            [(i,oo)  for i in range(1,r)] +
            [(i,i-1) for i in range(1,r+1)]
            )
        # Total number of pairs: 2 * r
        self.integrand = (
            (1,) + (2*r-1)*(0,),
            (self.d-r+1,) + (r-1) * (-1,) + r * (+1,)
            )
        self.datum = IgusaDatum(F + [LaurentIdeal(gens=[], RS=self.RS, ring=FractionField(actual_ring))]).simplify()
        return self.datum

    def padically_evaluate(self, shuffle=False):
        if self.root() is None:
            return SR(1)
        return ((1 - SR('q')**(-1))**(-1) * LocalZetaProcessor.padically_evaluate(self, shuffle=shuffle)).factor()

    def __repr__(self):
        if self.root() is not None:
            s = 'Ask processor:\n'
            s += 'Base ring: %s\n' % self.datum.ring
            s += 'R =\n' + str(self.R) + '\n'
            s += 'd = %d\n' % self.d
            s += 'e = %d\n' % self.e
            s += 'r = %d\n' % self.r
            s += 'Root:\n%s\n' % self.datum
            s += 'Pairs: ' + str(self.pairs) + '\n'
            s += 'Integrand: ' + str(self.integrand)
            return s
        else:
            return 'Trivial ask processor'
