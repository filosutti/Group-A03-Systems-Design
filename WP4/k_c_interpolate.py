import scipy as sp
from scipy import interpolate

# using loaded edges clamped so the dotted line 
# For test case A 

def k_c_value(a_b_value):
    a_b = []
    k_c = []

    f = sp.interpolate.interp1d(a_b, k_c, kind = "cubic", fill_value = "extrapolate")
    return f(a_b_value)
