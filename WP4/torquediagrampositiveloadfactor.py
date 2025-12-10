import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import math as m

# -----------------------------
# Load inputs
# -----------------------------
from TL import LperSpan0, MperSpan0

L = 11.89   # Half-span of the wing

# -----------------------------
# Aerodynamic moment arm: Distance between flexural axis and aerodynamic center
# CCW = +
# -----------------------------
def d(x):
    c_r = 4.02
    span = 11.89
    taper = 0.316

    c_t = c_r * taper
    chord = c_r - (c_r - c_t) * (x / span)
    return 0.20 * chord

# -----------------------------
# Interpolated aerodynamic loads from XFLR5 data
# -----------------------------
Lift   = LperSpan0
Moment = MperSpan0  # Pitching moment distribution from XFLR5

# -----------------------------
# Distributed torque densities
# -----------------------------
def tau_l(x):
    return abs(Lift(x) * d(x))   # Positive torque (CCW) for positive lift (+g)

def tau_m(x):
    return abs(Moment(x))        # Positive torque (CCW); keep as provided

# -----------------------------
# Engine point torque
# -----------------------------
w_engine    = 4800 * 0.45359237 * 9.81   # N  
thrust_arm  = 2.32 + 0.3
engine_arm  = 2.495
x_engine    = 3.75

T_thrust = 83.1e3

MomentPoint = abs((w_engine * engine_arm) - (T_thrust * thrust_arm))

# -----------------------------
# Root torque T0 – ensures T(L)=0
# -----------------------------
def T0_calc():
    tl, _ = quad(tau_l, 0, L)
    tm, _ = quad(tau_m, 0, L)
    return tl + MomentPoint - tm

T0 = T0_calc()

# -----------------------------
# Internal torque distribution (RENAMED)
# -----------------------------
def torque_pos_loadfactor(x):
    tl, _ = quad(tau_l, 0, x)
    tm, _ = quad(tau_m, 0, x)
    tpoint = MomentPoint if x >= x_engine else 0.0
    return -T0 + tl - tm + tpoint

