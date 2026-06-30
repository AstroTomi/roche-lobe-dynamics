# roche-lobe-dynamics
# Copyright (C) 2026 Tomás Andrés Cáceres-Mansilla
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
The simulation initializes with the 2 mass sources opposite to each other along the x axis.

? Mass transfer is a conservative process, so it obeys the conservation laws.
? The quantity MASS is conserved, so d(MASS_1 + MASS_2)/dt = 0.

TODO: Automate the process when Flag = True
"""

# Modules.
import numpy as np
import matplotlib.pyplot as plt
import time

# Definition of functions and variables.
from variables import A, MASS_1, MASS_2, X_1, X_2, MASS_TRANSF_1, X_RES, Y_RES  # Simulation parameters.
from variables import X_AXIS_LABEL, Y_AXIS_LABEL, PLOT_TITLE, COLORBAR_LABEL    # Plot labels.
from variables import BASE_PATH                                                 # Miscellaneous.

from functions import orb_ang_freq, eff_grav_pot

from flags import PRINT_LOG, SAVE_LOG, SAVE_FRAMES

# Time domain and time step.
T = np.linspace(0, 50, 1000); ts = T[1] - T[0]

# Definition of the meshgrid.
X = np.linspace(-2.5 * A, 2.5 * A, X_RES)
Y = np.linspace(-2.5 * A, 2.5 * A, Y_RES)
X_GRID, Y_GRID = np.meshgrid(X, Y)

# Distance from each point to center of mass.
r = (X_GRID**2 + Y_GRID**2)**0.5

# Direction of mass transference for source 2.
MASS_TRANSF_2 = -MASS_TRANSF_1

# * ==============
# * INITIAL VALUES
# * ==============

# Initial angular frequency.
OMEGA = orb_ang_freq(MASS_1, MASS_2, A)

# Initial semi-major axis.
a_t = A

# Initial masses.
mass_1_t = MASS_1
mass_2_t = MASS_2

# Initial position from point to sources.
S_1 = ((X_GRID - X_1)**2 + Y_GRID**2)**0.5
S_2 = ((X_GRID - X_2)**2 + Y_GRID**2)**0.5

# Initial potential (for colormap)
POT_GRID_INIT = eff_grav_pot(MASS_1, MASS_2, S_1, S_2, r, OMEGA)

# Definition of maximum and minimum values for the colormap.
v_min = np.percentile(POT_GRID_INIT, 5)
v_max = np.percentile(POT_GRID_INIT, 95)

# * ==========================================================================
# * TIME ITERATION. THIS INVOLVE:
# * MASS TRANSFERENCE, SEMI-MAJOR AXIS CHANGE AND DISTANCE FROM ORIGIN CHANGE.
# * ==========================================================================

# Definition of the figure
fig = plt.figure()

for index in range(len(T)):
    
    # Timestamp for logs.
    TIMESTAMP = time.strftime("%Y-%m-%d_%H:%M:%S")
    LOG_NAME = f"log_[{TIMESTAMP}].txt"
    
    # Clear the figure for iterations
    fig.clear()
    
    # This is only the core mechanism.
    mass_1_t = mass_1_t + MASS_TRANSF_1 * ts
    mass_2_t = mass_2_t + MASS_TRANSF_2 * ts
    if (mass_2_t <= 0.05) or (mass_1_t <= 0.05):    
        if PRINT_LOG:
            print(f"[{TIMESTAMP}] Mass threshold reached, terminating simulation...")
        if SAVE_LOG:
            with open(BASE_PATH / f"logs/{LOG_NAME}", "a") as log:
                log.write(f"[{TIMESTAMP}] Mass threshold reached, terminating simulation...")
        break

    # Differential change in semi-major axis.
    da = 2 * a_t * MASS_TRANSF_1 * ((1 / mass_2_t) - (1 / mass_1_t))

    # Differential change in semi-major axis.
    a_t = a_t + da * (T[1] - T[0])

    # Differential change in position.
    x_1_t = -a_t * (mass_2_t / (mass_1_t + mass_2_t))
    x_2_t = a_t * (mass_1_t / (mass_1_t + mass_2_t))

    # Distance from each point to sources.
    s_1 = ((X_GRID - x_1_t)**2 + Y_GRID**2)**0.5
    s_2 = ((X_GRID - x_2_t)**2 + Y_GRID**2)**0.5

    # Orbital angular frequency.
    omega_t = orb_ang_freq(mass_1_t, mass_2_t, a_t)

    # Calculus of the potential.
    POT_GRID = eff_grav_pot(mass_1_t, mass_2_t, s_1, s_2, r, omega_t)

    # Plotting.
    p = fig.add_subplot(1, 1, 1)
    
    colormesh = p.pcolormesh(
        X_GRID, Y_GRID, POT_GRID,
        vmin = v_min, vmax = v_max,
        cmap = 'plasma', rasterized = True
        )
    plt.colorbar(colormesh, ax = p, label = COLORBAR_LABEL)

    # Contour levels.
    levels = np.linspace(v_min * 0.75, 0, 50)
    p.contour(
        X_GRID, Y_GRID, POT_GRID,
        levels = levels, colors = 'black',
        linewidths = 1.0, linestyles = '-', alpha = 0.2 
        )

    # Position of sources, introduced a normalization for better view.
    p.scatter(x_1_t, 0, color = 'black', s = 50 * mass_1_t / (mass_1_t + mass_2_t))
    p.scatter(x_2_t, 0, color = 'black', s = 50 * mass_2_t / (mass_1_t + mass_2_t))

    # Details.
    p.set_xlim(-1.75 * A, 1.75 * A) ; p.set_ylim(-1.75 * A, 1.75 * A)
    p.set_xlabel(X_AXIS_LABEL); p.set_ylabel(Y_AXIS_LABEL)
    p.set_title(PLOT_TITLE)

    # Output.
    plt.axis('equal')
    plt.tight_layout()
    if SAVE_FRAMES:
        plt.savefig(BASE_PATH / f"out/output{index}.pdf")
    plt.pause(.05)
    
    # Stop the simulation if one of the masses gets too far.
    if (np.abs(x_1_t) > 2.25 * A) or (np.abs(x_2_t) > 2.25 * A):
        if PRINT_LOG:
            print(f"[{TIMESTAMP}] Sources too far away, terminating simulation...")
        if SAVE_LOG:
            with open(BASE_PATH / f"logs/{LOG_NAME}", "a") as log:
                log.write(f"[{TIMESTAMP}] Sources too far away, terminating simulation...")
        break
    
plt.pause(2)
print("Simulation has ended.")
