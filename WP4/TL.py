import scipy as sp
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np

from vn_diagram import n_ult

V_inf = 60
q = 1/2*1.225*V_inf*V_inf
W = 27719*9.80665
S = 62.8

def c(y):
    cr = 4.02
    ct = 1.27
    b = 23.78
    c = ct + (cr - ct)*(b/2 - y)*2/b
    return c

ylst0 = []
cllst0 = []
cdlst0 = []
cmlst0 = []
ylst10 = []
cllst10 = []
cdlst10 = []
cmlst10 = []
with open ('WP4/XFLR0.txt','r') as f:
    for line in f:
        parts = line.split()
        if len(parts) < 8:    # <-- skip blank / malformed lines
            continue
        yval = float(parts[0])
        cl = float(parts[3])
        cd = float(parts[5])   
        cm = float(parts[7])   
        ylst0.append(yval)
        cllst0.append(cl)
        cdlst0.append(cd)
        cmlst0.append(cm)
with open ('WP4/XFLR10.txt','r') as g:
    for line in g:
        parts = line.split()
        if len(parts) < 8:    # <-- skip blank / malformed lines
            continue
        yval = float(parts[0])
        cl = float(parts[3])
        cd = float(parts[5])   
        cm = float(parts[7])   
        ylst10.append(yval)
        cllst10.append(cl)
        cdlst10.append(cd)
        cmlst10.append(cm)
    #below takes y as parameter and yields the spanwise cl, cdi and cm
    cl_int_0 = sp.interpolate.interp1d(ylst0, cllst0, kind='cubic', fill_value="extrapolate")
    cd_int_0 = sp.interpolate.interp1d(ylst0, cdlst0, kind='cubic', fill_value="extrapolate")
    cm_int_0 = sp.interpolate.interp1d(ylst0, cmlst0, kind='cubic', fill_value="extrapolate")
    #below takes y as parameter and yields the spanwise cl, cdi and cm
    cl_int_10 = sp.interpolate.interp1d(ylst10, cllst10, kind='cubic', fill_value="extrapolate")
    cd_int_10 = sp.interpolate.interp1d(ylst10, cdlst10, kind='cubic', fill_value="extrapolate")
    cm_int_10 = sp.interpolate.interp1d(ylst10, cmlst10, kind='cubic', fill_value="extrapolate")

def LperSpan0(y):
    n_ult = 3.75
    cL0 = 0.304
    cL10 = 1.15

    L = n_ult*W
    cL = L/q/S
    aoa =  (cL-cL0)/(cL10-cL0)*10
    cly = (cl_int_10(y)-cl_int_0(y))*aoa/10 + cl_int_0(y)
    LperSpan = cly*q*c(y)
    return LperSpan

def MperSpan0(y):
    n_ult = 3.75
    cL0 = 0.304
    cL10 = 1.15
    L = n_ult*W
    cL = L/q/S
    aoa =  (cL-cL0)/(cL10-cL0)*10
    cmy = (cm_int_10(y)-cm_int_0(y))*aoa/10 + cm_int_0(y)
    MperSpan = cmy*q*c(y)*c(y)
    return MperSpan

def LperSpan1(y):
    n_ult = -1.5
    cL0 = 0.304
    cL10 = 1.15
    L = n_ult*W
    cL = L/q/S
    aoa =  (cL-cL0)/(cL10-cL0)*10
    cly = (cl_int_10(y)-cl_int_0(y))*aoa/10 + cl_int_0(y)
    LperSpan = cly*q*c(y)
    return LperSpan

def MperSpan1(y):
    n_ult = -1.5
    cL0 = 0.304
    cL10 = 1.15
    L = n_ult*W
    cL = L/q/S
    aoa =  (cL-cL0)/(cL10-cL0)*10
    cmy = (cm_int_10(y)-cm_int_0(y))*aoa/10 + cm_int_0(y)
    MperSpan = cmy*q*c(y)*c(y)
    return MperSpan

# Create a spanwise grid from root (0) to tip (b/2)
b = 23.78
y_vals = np.linspace(0, b/2, 300)

# Compute distributions
L0_vals = np.array([LperSpan0(y) for y in y_vals])
L1_vals = np.array([LperSpan1(y) for y in y_vals])
M0_vals = np.array([MperSpan0(y) for y in y_vals])
M1_vals = np.array([MperSpan1(y) for y in y_vals])

# -------------------------------
# Plot Lift distributions
# -------------------------------
#plt.figure(figsize=(10,5))
#plt.plot(y_vals, L0_vals, label='L per span (n=3.75)')
#plt.plot(y_vals, L1_vals, label='L per span (n=-1.5)')
#plt.title("Lift Distribution Along the Span")
#plt.xlabel("Spanwise position y [m]")
#plt.ylabel("Lift per span [N/m]")
#plt.grid(True)
#plt.legend()

# -------------------------------
# Plot Moment distributions
# -------------------------------
#plt.figure(figsize=(10,5))sw
#plt.plot(y_vals, M0_vals, label='M per span (n=3.75)')
#plt.plot(y_vals, M1_vals, label='M per span (n=-1.5)')
#plt.title("Moment Distribution Along the Span")
#plt.xlabel("Spanwise position y [m]")
#plt.ylabel("Moment per span [Nm/m]")
#plt.grid(True)
#plt.legend()

#plt.show()
