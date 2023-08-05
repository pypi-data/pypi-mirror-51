# -*- coding: utf-8 -*-
"""
The L-Lake model defines the methods and classes required for
performing lake and dam retention processes as implemented in
LARSIM.
"""
# import...
# ...from HydPy
from hydpy.exe.modelimports import *
# ...from llake
from hydpy.models.llake.llake_control import ControlParameters
from hydpy.models.llake.llake_derived import DerivedParameters
from hydpy.models.llake.llake_fluxes import FluxSequences
from hydpy.models.llake.llake_states import StateSequences
from hydpy.models.llake.llake_inlets import InletSequences
from hydpy.models.llake.llake_outlets import OutletSequences
from hydpy.models.llake.llake_aides import AideSequences
from hydpy.models.llake.llake_model import Model

tester = Tester()
cythonizer = Cythonizer()
cythonizer.finalise()
