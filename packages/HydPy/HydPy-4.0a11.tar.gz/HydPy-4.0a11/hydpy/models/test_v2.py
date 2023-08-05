# -*- coding: utf-8 -*-
# pylint: disable=line-too-long, wildcard-import, unused-wildcard-import
"""This simple test model is thought for testing numerical integration
strategies.  It can be seen from two perspectives.  On the one hand
it implements a simple discontinous equation, bringing numerical integration
algorithms into trouble.  On the other hand it describes a simple storage
with a loss that is constant over time, as long as some storage content is
left.  The loss rate |Q| and the initial storage content |S| can be set as
required.
"""
# imports...
# ...from HydPy
from hydpy.exe.modelimports import *
from hydpy.core import modeltools
from hydpy.core import parametertools
from hydpy.core import sequencetools
# ...from test
from hydpy.models.test import test_model
from hydpy.models.test import test_control
from hydpy.models.test import test_solver
from hydpy.models.test import test_fluxes
from hydpy.models.test import test_states


class Model(modeltools.ELSModel):
    """Test model, Version 2."""
    INLET_METHODS = ()
    RECEIVER_METHODS = ()
    PART_ODE_METHODS = (test_model.calc_q_v2,)
    FULL_ODE_METHODS = (test_model.calc_s_v1,)
    OUTLET_METHODS = ()
    SENDER_METHODS = ()


class ControlParameters(parametertools.SubParameters):
    """Control parameters of Test model, Version 2."""
    CLASSES = (test_control.K,)


class SolverParameters(parametertools.SubParameters):
    """Solver parameters of the Test model,."""
    CLASSES = (test_solver.AbsErrorMax,
               test_solver.RelDTMin)


class FluxSequences(sequencetools.FluxSequences):
    """Flux sequences of Test model, Version 2."""
    CLASSES = (test_fluxes.Q,)


class StateSequences(sequencetools.StateSequences):
    """State sequences of Test model, Version 2."""
    CLASSES = (test_states.S,)


tester = Tester()
cythonizer = Cythonizer()
cythonizer.finalise()
