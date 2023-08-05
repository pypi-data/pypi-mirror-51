# -*- coding: utf-8 -*-
"""
The L-Land model is the core of the HydPy implementation of the
LARSIM model.  It consists of routines for the preparation
of meteorological input, the calculation of potential evaporation,
the simulation of water stored on plants, in the snow layer and in the
soil, as well as runoff concentration.
"""
# import...
# ...from HydPy
from hydpy.exe.modelimports import *
# ...from lland
from hydpy.models.lland.lland_constants import (
    SIED_D, SIED_L, VERS, ACKER, WEINB, OBSTB, BODEN, GLETS, GRUE_I, FEUCHT,
    GRUE_E, BAUMB, NADELW, LAUBW, MISCHW, WASSER, FLUSS, SEE)
from hydpy.models.lland.lland_control import ControlParameters
from hydpy.models.lland.lland_derived import DerivedParameters
from hydpy.models.lland.lland_inputs import InputSequences
from hydpy.models.lland.lland_fluxes import FluxSequences
from hydpy.models.lland.lland_states import StateSequences
from hydpy.models.lland.lland_logs import LogSequences
from hydpy.models.lland.lland_aides import AideSequences
from hydpy.models.lland.lland_outlets import OutletSequences
from hydpy.models.lland.lland_model import Model

tester = Tester()
cythonizer = Cythonizer()
cythonizer.finalise()
