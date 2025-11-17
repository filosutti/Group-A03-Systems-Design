import scipy as sp
from scipy import interpolate

ylst = []
cllst = []
cdlst = []
cmlst = []



with open ('WP4/XFLR0.txt','r') as f:
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

cl_int = sp.interpolate.interp1d(ylst, cllst, kind='cubic', fill_value="extrapolate")
cd_int = sp.interpolate.interp1d(ylst, cdlst, kind='cubic', fill_value="extrapolate")
cm_int = sp.interpolate.interp1d(ylst, cmlst, kind='cubic', fill_value="extrapolate")
