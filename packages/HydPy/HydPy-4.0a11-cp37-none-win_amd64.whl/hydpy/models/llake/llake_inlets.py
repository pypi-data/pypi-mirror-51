# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: enable=missing-docstring

# import...
# ...from HydPy
from hydpy.core import sequencetools


class Q(sequencetools.LinkSequence):
    """Abfluss (runoff) [m³/s]."""
    NDIM, NUMERIC = 1, False


class InletSequences(sequencetools.LinkSequences):
    """Upstream link sequences of HydPy-L-Lake."""
    CLASSES = (Q,)
