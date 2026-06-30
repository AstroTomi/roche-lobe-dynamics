"""
Eventually, you will not need to edit this file, as it should contain every analytic function and numeric solver for future equations.

TODO: [ ] Implement a class for objects like stars, planets or black holes.
TODO: [ ] Include a numeric solve for Roche radius approximation.
TODO: [ ] Units and quantity support (astropy).
"""

from variables import G

def orb_ang_freq(mass_1:float, mass_2:float, a:float) -> float:
    """_Calculates the orbital angular velocity._

    Args:
        mass_1 (_float_): _Mass of source 1._
        mass_2 (_float_): _Mass of source 2._
        a (_float_): _Semi-major axis._

    Returns:
        _float_: _Orbital angular velocity._
    """
    return (G * (mass_1 + mass_2) / a**3) ** 0.5

def eff_grav_pot(mass_1:float, mass_2:float, s_1:float, s_2:float, r:float, omega:float) -> float:
    """_Calculates the effective gravitational potential energy on a point._

    Args:
        mass_1 (float): _Mass of source 1._
        mass_2 (float): _Mass of source 2._
        s_1 (float): _Distance from point to source 1._
        s_2 (float): _Distance from point to source 2._
        r (float): _Distance from point to center of mass._
        omega (float): _Orbital angular frequency, must include this variable as a result from function: "orb_anf_freq()"._

    Returns:
        float: _Effective gravitational potential on point._
    """
    return -G * ((mass_1 / s_1) + (mass_2 / s_2)) - 0.5 * omega**2 * r**2