"""zb_model — clean-room flight-model math for Project Z!B's sub-250g UAV family.

Every module implements Z!B-authored analysis only. No ArduPilot code is
copied anywhere in this package. Constants that are engineering estimates
are marked ``# Z!B-ESTIMATED:`` and registered in
``zb_model/data/assumptions.yaml``.
"""

from zb_model import drag, mission, propulsion, stability, structures, trim, weight

__all__ = ["drag", "mission", "propulsion", "stability", "structures", "trim", "weight"]
__version__ = "0.1.0"
