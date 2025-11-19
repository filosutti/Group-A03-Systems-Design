import scipy as sp
from scipy import interpolate

V_inf = 228.17
q = 1/2*1.225*V_inf*V_inf

ylst0 = []
cllst0 = []
cdlst0 = []
cmlst0 = []


def c(y):
    cr = 4.02
    ct = 1.27
    b = 23.78
    c = ct + (cr - ct)*(b/2 - y)*2/b
    return c

with open ('WP4/XFLR0.txt','r') as f:
    for line in f:
        parts = line.split()

        y = float(parts[0])
        cl = float(parts[3])
        cd = float(parts[5])   
        cm = float(parts[7])   

        ylst0.append(y)
        cllst0.append(cl)
        cdlst0.append(cd)
        cmlst0.append(cm)

print("ylst", ylst0)
print("clst", cllst0)
print("cdlst", cdlst0)
print("cmlst", cmlst0)

#below takes y as parameter and yields the spanwise cl, cdi and cm
cl_int_0 = sp.interpolate.interp1d(ylst0, cllst0, kind='cubic', fill_value="extrapolate")
cd_int_0 = sp.interpolate.interp1d(ylst0, cdlst0, kind='cubic', fill_value="extrapolate")
cm_int_0 = sp.interpolate.interp1d(ylst0, cmlst0, kind='cubic', fill_value="extrapolate")

with open ('WP4/XFLR10.txt','r') as f:
    for line in f:
        parts = line.split()

        y = float(parts[0])
        cl = float(parts[3])
        cd = float(parts[5])   
        cm = float(parts[7])   

        ylst.append(y)
        cllst.append(cl)
        cdlst.append(cd)
        cmlst.append(cm)

print("ylst", ylst)
print("clst", cllst)
print("cdlst", cdlst)
print("cmlst", cmlst)

#below takes y as parameter and yields the spanwise cl, cdi and cm
cl_int_0 = sp.interpolate.interp1d(ylst, cllst, kind='cubic', fill_value="extrapolate")
cd_int_0 = sp.interpolate.interp1d(ylst, cdlst, kind='cubic', fill_value="extrapolate")
cm_int_0 = sp.interpolate.interp1d(ylst, cmlst, kind='cubic', fill_value="extrapolate")