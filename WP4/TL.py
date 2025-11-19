import scipy as sp
from scipy import interpolate

V_inf = 228.17
q = 1/2*1.225*V_inf*V_inf

ylst0 = []
cllst0 = []
cdlst0 = []
cmlst0 = []
ylst10 = []
cllst10 = []
cdlst10 = []
cmlst10 = []

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