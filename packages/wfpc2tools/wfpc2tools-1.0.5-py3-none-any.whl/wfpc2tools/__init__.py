"""The wfpc2tools package holds Python tasks useful for analyzing WFPC2 data.

These tasks include:
      WFPC2CTE - computes the CTE degradation & updates header keywords

      
This release also includes alpha versions of the following tasks:
     Wfpc2destreak - Calculate magnitude of, and remove, streaks from data

Utility and library functions used by these tasks are also included in this
module.


"""
from __future__ import absolute_import

from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = 'UNKNOWN'

from . import wfpc2cte
from . import wfpc2destreak
