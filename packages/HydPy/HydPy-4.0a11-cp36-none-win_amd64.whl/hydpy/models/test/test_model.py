# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: enable=missing-docstring

# imports...
# ...from HydPy
from hydpy.core import modeltools


def calc_q_v1(self):
    """Calculate the actual storage loss.

    This simple equation is continuous but potentially stiff.

    Required control parameter:
      |K|

    Required state sequence:
     |S|

    Calculated flux sequence:
      |Q|

    Basic equation:
      :math:`Q = K \\cdot S`

    Example:

       >>> from hydpy.models.test import *
       >>> parameterstep()
       >>> k(0.5)
       >>> states.s = 2.0
       >>> model.calc_q_v1()
       >>> fluxes.q
       q(1.0)
    """
    con = self.parameters.control.fastaccess
    flu = self.sequences.fluxes.fastaccess
    sta = self.sequences.states.fastaccess
    flu.q = con.k*sta.s


def calc_q_v2(self):
    """Calculate the actual storage loss.

    This simple equation is discontinuous.

    Required control parameter:
      |K|

    Required state sequence:
      |S|

    Calculated flux sequence:
      |Q|

    Basic equation:
      :math:`Q = \\Bigl \\lbrace
      {
      {K \\ | \\ S > 0}
      \\atop
      {0 \\ | \\ S \\leq 0}
      }`

    Examples:

       >>> from hydpy.models.test import *
       >>> parameterstep()
       >>> k(0.5)
       >>> states.s = 2.0
       >>> model.calc_q_v2()
       >>> fluxes.q
       q(0.5)
       >>> states.s = -1.0
       >>> model.calc_q_v2()
       >>> fluxes.q
       q(0.0)
    """
    con = self.parameters.control.fastaccess
    flu = self.sequences.fluxes.fastaccess
    sta = self.sequences.states.fastaccess
    if sta.s > 0.:
        flu.q = con.k
    else:
        flu.q = 0.


def calc_s_v1(self):
    """Calculate the actual storage content.

    Required flux sequence:
      |Q|

    Calculated state sequence:
     |S|

    Basic equation:
      :math:`\\frac{dS}{dt} = Q`

    Example:

       >>> from hydpy.models.test import *
       >>> parameterstep()
       >>> states.s.old = 1.0
       >>> fluxes.q = 0.8
       >>> model.calc_s_v1()
       >>> states.s
       s(0.2)
    """
    flu = self.sequences.fluxes.fastaccess
    old = self.sequences.states.fastaccess_old
    new = self.sequences.states.fastaccess_new
    new.s = old.s-flu.q


class Model(modeltools.ELSModel):
    """Test model."""
    INLET_METHODS = ()
    RECEIVER_METHODS = ()
    PART_ODE_METHODS = (calc_q_v1,
                        calc_q_v2)
    FULL_ODE_METHODS = (calc_s_v1,)
    OUTLET_METHODS = ()
    SENDER_METHODS = ()
