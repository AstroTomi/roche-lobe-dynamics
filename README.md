# Roche Lobe Dynamics Simulator

A modular, Python-based numerical simulation of binary star systems undergoing conservative mass transfer. This project dynamically models and visualizes the evolution of the effective gravitational potential, Roche lobe topology, and orbital mechanics of a binary system over time.

This project is a work in progress. If you have any intention of collaborating, debugging the code or leaving a comment, please contact me via [email](mailto:tomasandrescaceresm+github@gmail.com?subject=roche-lobe-dynamics) or open an issue in this repository. Also, if you want to learn more about the physics behind this, check the references below! It'll be appreciated if you leave a star on the repository.

## Overview

In close binary star systems, stellar evolution can lead to one star filling its Roche lobe, initiating a transfer of mass to its companion through the inner Lagrangian point (L1). Assuming a conservative mass transfer process (where total mass and total orbital angular momentum are conserved), this simulator integrates the resulting differential equations to model how the semimajor axis, angular frequency, and effective potential respond to this mass exchange.

## Features

* **Dynamic Orbital Evolution:** Calculates the real-time expansion or contraction of the semimajor axis based on the mass ratio and mass transfer rate.
* **Effective Potential Mapping:** Computes and plots the 2D equipotential surfaces (Roche lobes) in the co-rotating reference frame, including the centrifugal force term.
* **Modular Architecture:** Clean separation of physical constants, mathematical definitions, execution flags, and the main integration loop.
* **Automated Halts:** Safely terminates the simulation if a mass threshold is breached or if the binary sources exceed the boundaries of the spatial grid.
* **Logging & Exporting:** Built-in toggles to print console logs, save logs to text files, and export individual simulation frames as `.pdf` files for external animation compiling.

## Future Implementations & Roadmap

This simulator establishes the foundational mechanics of conservative binary mass transfer. Future updates will focus on expanding the physical accuracy, numerical stability, and thermodynamic scope of the model. Planned features include:

* **Analytic Roche Lobe Limits (Eggleton's Approximation):** Implement dynamic thresholding using Eggleton's formula for the Roche lobe radius ($R_L$). This will allow the simulation to automatically halt or reverse mass transfer when the donor star's physical radius shrinks within its Roche limit, simulating the transition between active accretion and detached phases.
* **Advanced Numerical Integrators (RK4):** Upgrade the current explicit Euler integration method to a 4th-order Runge-Kutta (RK4) scheme. This will significantly reduce truncation errors and improve the long-term stability of the orbital semi-major axis and angular frequency calculations.
* **Non-Conservative Mass Transfer:** Introduce parameterized mass and angular momentum loss from the system, simulating phenomena such as stellar winds, isotropic ejections, or circumbinary disk formation.
* **Thermodynamic Radius Evolution:** Couple the mass transfer rate ($\dot{M}$) to the thermal adjustment timescale (Kelvin-Helmholtz timescale) of the donor star, allowing for dynamic calculation of the stellar radius as it responds to mass loss.
* **Rendering Optimization:** Implement `matplotlib` blitting techniques to optimize the rendering loop, drastically increasing the frame rate for live animation plotting.

## Project Structure

* `roche-lobe-dynamics.py`: The main execution script containing the time-domain loop, Euler integration, and `matplotlib` rendering.
* `functions.py`: Pure mathematical functions for calculating the orbital angular frequency and the effective gravitational potential.
* `variables.py`: Configuration file for physical parameters, initial conditions, grid resolution, and plot labeling.
* `flags.py`: Boolean toggles for managing output behavior (logging and frame saving).
* `logs/`: Logs directory.
* `out/`: Outputs folder for each time iteration.

## Mathematical Background

The simulation relies on the conservation of total mass ($M_1 + M_2 = \text{const}$) and orbital angular momentum. The rate of change of the semimajor axis ($a$) is driven by the differential equation:

$$\frac{da}{dt} = 2 a \dot{M}_1 \left( \frac{1}{M_2} - \frac{1}{M_1} \right)$$

The effective gravitational potential ($\Phi_{\text{eff}}$) in the co-rotating frame is evaluated at each spatial point $r$ as:

$$\Phi_{\text{eff}} = -G \left( \frac{M_1}{s_1} + \frac{M_2}{s_2} \right) - \frac{1}{2}\omega^2 r^2$$

Where $s_1$ and $s_2$ are the distances from the evaluated point to each respective mass, and $\omega$ is the orbital angular frequency given by Kepler's Third Law.

### References

* **Frank, J., King, A., & Raine, D. J.** (2002). *Accretion Power in Astrophysics* (3rd ed.). Cambridge University Press.
* **Pringle, J. & King, A.** (2007). *Astrophysical Flows* (1st ed.). Cambridge University Press. 
* **Carroll, B. W., & Ostlie, D. A.** (2014). *An Introduction to Modern Astrophysics* (2nd ed.). Cambridge University Press.

## Usage

### Prerequisites
Ensure you have Python installed along with the following standard scientific libraries:
* `numpy`
* `matplotlib`

A virtual environment `.venv` is recommended.

### Configuration
1.  Open `variables.py` to set your desired initial masses (`MASS_1`, `MASS_2`), initial semimajor axis (`A`), and the constant mass transfer rate (`MASS_TRANSF_1`). 
    * *Note: If Source 1 is the donor (losing mass), `MASS_TRANSF_1` must be a negative value.*
2.  Open `flags.py` to toggle `PRINT_LOG`, `SAVE_LOG`, or `SAVE_FRAMES` depending on whether you want to observe the live simulation or render it to disk.

### Execution
Run the main script from your terminal on the `roche-lobes-dynamics/` folder:
```bash
python roche-lobe-dynamics.py
```