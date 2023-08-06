"""
Triangulations of pointed cones; includes yet another interface to Normaliz.
"""

from __future__ import absolute_import, division
from sage.all import *
from sage.features import Executable

from . import common
from collections import namedtuple
from shutil import rmtree

import os
import subprocess

from .util import TemporaryDirectory, cd, my_find_executable, augmented_env

from .tmplist import TemporaryList

from .util import create_logger
logger = create_logger(__name__)

# TODO: Consider using the Sage Normaliz interface that uses PyNormaliz.
_normaliz_exe = Executable('Normaliz',
                            executable='normaliz',
                            spkg='normaliz',
                            url='https://www.normaliz.uni-osnabrueck.de')
if not _normaliz_exe.is_present():
    logger.warning('Normaliz not found. '
                'Triangulation will be slow. '
                'You can try to install it by running "sage -i normaliz"')

# A simplicial cone 'sc' can be turned into an honest one
# via Cone(rays=sc.rays, lattice=ZZ**ambdim, check=False)).

SCONE = namedtuple('SCONE', ['rays', 'multiplicity'])
from .surf import SURF

def _explode_vector(v):
    if len(v) == 0:
        return ''
    elif len(v) == 1:
        return str(v[0])
    else:
        return ' '.join('%d' % (a,) for a in v[:-1]) + ' ' + str(v[-1])

def _normalise_cone(C):
    """
    Produce valid normaliz input from cone ``C``.
    """
    s = '%d\n%d\n' % (C.nrays(), C.lattice_dim())
    for r in C.rays():
        s += _explode_vector(r) + '\n'
    return s + 'integral_closure\n'

def _triangulate_cone_internal(C, all_cones=False):
    rays = list(C.rays())
    if any(a < 0 for r in rays for a in r):
        raise ValueError('Internal triangulation only implemented for non-negative cones.')
    normalised_rays = [Integer(1)/v.norm(1) * vector(QQ,v) for v in rays]

    with TemporaryList() as maximal_faces:
        for indices in PointConfiguration(normalised_rays).triangulate() if len(normalised_rays) > 1 else [[0]]:
            subrays = [rays[i] for i in indices]
            if all_cones:
                maximal_faces.append(indices)
            else:
                multiplicity = prod(a for a in matrix(ZZ,subrays).elementary_divisors() if a != 0)
                yield SCONE(rays=subrays, multiplicity=multiplicity)

        if all_cones:
            X = SimplicialComplex(maximal_faces=maximal_faces, maximality_check=False)
            for f in X.face_iterator():
                yield SCONE(rays = [rays[i] for i in f], multiplicity=-1)

def _triangulate_cone_normaliz(C, all_cones):
    if all_cones:
        raise NotImplementedError

    with TemporaryDirectory() as tmpdir:
        logger.debug('Temporary directory of this normaliz session: %s', tmpdir)

        play = os.path.join(tmpdir, 'play')
        with open(play + '.in', 'wb') as f:
            f.write(_normalise_cone(C).encode("ascii"))

        with cd(tmpdir), open(os.devnull, 'wb') as DEVNULL:
            retcode = subprocess.call(
                [common.normaliz, '-B', '-t', '-T', '-x=1', play],
                stdout=DEVNULL, stderr=DEVNULL,
                env=augmented_env(common.normaliz)
                )
        if retcode != 0:
            raise RuntimeError('Normaliz failed')

        with TemporaryList() as maximal_faces:
            # Recover all the rays from the triangulation
            with TemporaryList() as rays:
                with open(play + '.tgn', 'rb') as f:
                    nrays = int(f.readline())
                    ambdim = int(f.readline())
                    rays = []
                    if ambdim != C.lattice_dim():
                        raise RuntimeError('The triangulation lives in the wrong space')
                    for line in f:
                        rays.append([int(w) for w in line.split()])

                    if len(rays) != nrays:
                        raise RuntimeError('Number of rays is off')
                    logger.debug('Total number of rays in triangulation: %d', nrays)

                # Recover the simplicial pieces
                cnt = 0
                with open(play + '.tri', 'rb') as f:
                    ncones = int(f.readline())
                    mplus1 = int(f.readline())

                    if mplus1 != C.dim() + 1:
                        raise RuntimeError('.tri and .tgn files do not match')
                    for line in f:
                        line = line.decode("ascii")
                        if line == 'plain\n':
                            continue
                        elif line == 'nested\n':
                            raise RuntimeError('Normaliz returned a nested triangulation; this should never happen')

                        cnt += 1
                        li = [int(w) for w in line.split()]
                        if li[-1] == -1:
                            raise RuntimeError('Multiplicity is missing from Normaliz output')

                        if all_cones:
                            maximal_faces.append([i-1 for i in li[:-1]])
                            # Note that we discard all multiplicities in this case.
                        else:
                            yield SCONE(rays = [rays[i-1] for i in li[:-1]],
                                        multiplicity = li[-1]
                                        )

            logger.debug('Total number of cones in triangulation: %d', cnt)
            if cnt != ncones:
                raise RuntimeError('Number of simplicial cones is off')

            if all_cones:
                X = SimplicialComplex(maximal_faces=maximal_faces, maximality_check=False)
                for f in X.face_iterator():
                    yield SCONE(rays = [rays[i] for i in f], multiplicity=-1)

def triangulate_cone(C, all_cones=False):
    if all_cones:
        raise NotImplementedError
    return _triangulate_cone_normaliz(C, all_cones) if common.normaliz else _triangulate_cone_internal(C, all_cones)

def _topologise_scone(sc, Phi):
    if not sc.rays:
        raise ValueError('Cannot handle empty scones')
    if (Phi.nrows() != len(sc.rays[0])) or (Phi.ncols() != 2):
        raise ValueError('Invalid substitution matrix')

    li = [(int(Phi.column(0)*vector(ZZ,v)),
           int(Phi.column(1)*vector(ZZ,v))) for v in sc.rays]

    # An element of 'li' of the form (0,b) is really just the
    # scalar -b in disguise (mind the sign!).
    # Collect all of those together, cancelling common factors
    # with the numerator sc.multiplicity.

    rays = []
    num, den = sc.multiplicity, 1
    for (a,b) in li: # this becomes 1/(a*s-b) in the SURF
        if a == 0:
            den *= (-b)
        else:
            rays.append((a,b))
    g = int(gcd(sc.multiplicity, den))
    num /= g
    den /= g

    if den == -1:
        num, den = -num, 1

    if den != 1:
        rays.append((0,-den))
    return SURF(scalar=num, rays=rays)

def topologise_cone(C, Phi):
    """
    Turn the cone 'C' into a generator of SURFs via the substitution matrix
    'Phi'.
    """

    if C.dim() == 0:
        raise RuntimeError
        # return iter([])
    else:
        return (_topologise_scone(sc, Phi) for sc in triangulate_cone(C))
