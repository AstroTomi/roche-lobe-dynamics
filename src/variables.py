"""
This file is intended to be edited at needed.
? You will be able to include units on every simulation parameter.
! Remember to include the units on the labels.

TODO: [ ] Implement a dynamic mass threshold trigger based on the analytic approximation for the Roche Lobe radius.
TODO: [ ] Introduce non-conservative mass transfer terms.
TODO: [ ] Implement dynamic contour leveling parameters.
TODO: [ ] Include units (astropy) support for the computational loop.
"""

# Modules.
from pathlib import Path

# * ======================
# * SIMULATION PARAMETERS.
# * ======================

# Gravitational constant.
G = 1.
# Masses.
MASS_1 = 3.
MASS_2 = 5.
# Initial distance between sources. Semi-major axis.
A = 200
# Constant mass transference rate, Source 2 donates to Source 1.
MASS_TRANSF_1 = 1 
# Initial distance from sources to center of mass.
X_2 = (MASS_1 * A / (MASS_1 + MASS_2))
# The '-' sign is introduced artificially to ensure the center of mass is on the origin and the sources are opposite from each other.
X_1 = - (A - X_2)
# Number of cells on each axis. so the total resolution is X_RES X Y_RES.
X_RES = 75
Y_RES = 75

# * ============
# * PLOT LABELS.
# * ============

PLOT_TITLE = ''
COLORBAR_LABEL = r'$\Phi$ [arb. unit]'
X_AXIS_LABEL = r'$X$ [arb. unit]'
Y_AXIS_LABEL = r'$Y$ [arb. unit]'

# * ==============
# * MISCELLANEOUS.
# * ==============

# Workspace directory.
BASE_PATH = Path(__file__).parents[1]