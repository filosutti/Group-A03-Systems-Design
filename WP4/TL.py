import scipy as sp
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np

#from vn_diagram import n_ult
n_ult = 3.75
V_inf = 228.17
q = 1/2*0.38*V_inf*V_inf
W = 27719*9.80665
S = 62.8
cL0 = 0.304
cL10 = 1.15
ylst0 = []
cllst0 = []
cdlst0 = []
cmlst0 = []
ylst10 = []
cllst10 = []
cdlst10 = []
cmlst10 = []
L = n_ult*W
cL = L/q/S
aoa =  (cL-cL0)*(cL10-cL0)*10
def c(y):
    cr = 4.02
    ct = 1.27
    b = 23.78
    c = ct + (cr - ct)*(b/2 - y)*2/b
    return c

with open ('WP4/XFLR0.txt','r') as f:
    for line in f:
        parts = line.split()
        if len(parts) < 8:    # <-- skip blank / malformed lines
            continue
        y = float(parts[0])
        cl = float(parts[3])
        cd = float(parts[5])   
        cm = float(parts[7])   

        ylst0.append(y)
        cllst0.append(cl)
        cdlst0.append(cd)
        cmlst0.append(cm)

print("ylst 0", ylst0)
print("clst 0", cllst0)
print("cdlst 0", cdlst0)
print("cmlst 0", cmlst0)

#below takes y as parameter and yields the spanwise cl, cdi and cm
cl_int_0 = sp.interpolate.interp1d(ylst0, cllst0, kind='cubic', fill_value="extrapolate")
cd_int_0 = sp.interpolate.interp1d(ylst0, cdlst0, kind='cubic', fill_value="extrapolate")
cm_int_0 = sp.interpolate.interp1d(ylst0, cmlst0, kind='cubic', fill_value="extrapolate")

with open ('WP4/XFLR10.txt','r') as g:
    for line in g:
        parts = line.split()
        if len(parts) < 8:    # <-- skip blank / malformed lines
            continue
        y = float(parts[0])
        cl = float(parts[3])
        cd = float(parts[5])   
        cm = float(parts[7])   

        ylst10.append(y)
        cllst10.append(cl)
        cdlst10.append(cd)
        cmlst10.append(cm)

print("ylst 10", ylst10)
print("clst 10", cllst10)
print("cdlst 10", cdlst10)
print("cmlst 10", cmlst10)

#below takes y as parameter and yields the spanwise cl, cdi and cm
cl_int_10 = sp.interpolate.interp1d(ylst10, cllst10, kind='cubic', fill_value="extrapolate")
cd_int_10 = sp.interpolate.interp1d(ylst10, cdlst10, kind='cubic', fill_value="extrapolate")
cm_int_10 = sp.interpolate.interp1d(ylst10, cmlst10, kind='cubic', fill_value="extrapolate")

print(cl_int_10(1)*q*c(1))

def LperSpan0(y):
    cly = (cl_int_10(y)-cl_int_0(y))*aoa/10 + cl_int_0(y)
    LperSpan = cly*q*c(y)
    return LperSpan
def MperSpan0(y):
    cmy = (cm_int_10(y)-cm_int_0(y))*aoa/10 + cm_int_0(y)
    MperSpan = cmy*q*c(y)*c(y)
    return MperSpan

# Use the spanwise stations from the dataset (positive half-span)
y_plot = np.array(ylst0)   # or ylst10, they should be the same

# Compute L' and M' at each y
L_values = [LperSpan0(y) for y in y_plot]
M_values = [MperSpan0(y) for y in y_plot]

# --- Plot L per span ---
plt.figure()
plt.plot(y_plot, L_values)
plt.xlabel("y [m]")
plt.ylabel("Lift per span L'(y)")
plt.title("Spanwise Lift Distribution")
plt.grid(True)

# --- Plot M per span ---
plt.figure()
plt.plot(y_plot, M_values)
plt.xlabel("y [m]")
plt.ylabel("Moment per span M'(y)")
plt.title("Spanwise Pitching Moment Distribution")
plt.grid(True)

plt.show()
