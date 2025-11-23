import scipy as sp
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np

from vn_diagram import n_ult

V_inf = 228.17
q = 1/2*0.38*V_inf*V_inf
W = 27719*9.80665
S = 62.8

def c(y):
    cr = 4.02
    ct = 1.27
    b = 23.78
    c = ct + (cr - ct)*(b/2 - y)*2/b
    return c


def LperSpan0(y):
    n_ult = 3.75
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
    aoa =  (cL-cL0)/(cL10-cL0)*10

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
    #below takes y as parameter and yields the spanwise cl, cdi and cm
    cl_int_0 = sp.interpolate.interp1d(ylst0, cllst0, kind='cubic', fill_value="extrapolate")
    cd_int_0 = sp.interpolate.interp1d(ylst0, cdlst0, kind='cubic', fill_value="extrapolate")
    cm_int_0 = sp.interpolate.interp1d(ylst0, cmlst0, kind='cubic', fill_value="extrapolate")

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
    cl_int_10 = sp.interpolate.interp1d(ylst10, cllst10, kind='cubic', fill_value="extrapolate")
    cd_int_10 = sp.interpolate.interp1d(ylst10, cdlst10, kind='cubic', fill_value="extrapolate")
    cm_int_10 = sp.interpolate.interp1d(ylst10, cmlst10, kind='cubic', fill_value="extrapolate")
    cly = (cl_int_10(y)-cl_int_0(y))*aoa/10 + cl_int_0(y)
    LperSpan = cly*q*c(y)
    return LperSpan

def MperSpan0(y):
    n_ult = 3.75
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
    aoa =  (cL-cL0)/(cL10-cL0)*10
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
    #below takes y as parameter and yields the spanwise cl, cdi and cm
    cl_int_0 = sp.interpolate.interp1d(ylst0, cllst0, kind='cubic', fill_value="extrapolate")
    cd_int_0 = sp.interpolate.interp1d(ylst0, cdlst0, kind='cubic', fill_value="extrapolate")
    cm_int_0 = sp.interpolate.interp1d(ylst0, cmlst0, kind='cubic', fill_value="extrapolate")

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
    cl_int_10 = sp.interpolate.interp1d(ylst10, cllst10, kind='cubic', fill_value="extrapolate")
    cd_int_10 = sp.interpolate.interp1d(ylst10, cdlst10, kind='cubic', fill_value="extrapolate")
    cm_int_10 = sp.interpolate.interp1d(ylst10, cmlst10, kind='cubic', fill_value="extrapolate")

    cmy = (cm_int_10(y)-cm_int_0(y))*aoa/10 + cm_int_0(y)
    MperSpan = cmy*q*c(y)*c(y)
    return MperSpan

def LperSpan1(y):
    n_ult = -1.5
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
    aoa =  (cL-cL0)/(cL10-cL0)*10
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
    #below takes y as parameter and yields the spanwise cl, cdi and cm
    cl_int_0 = sp.interpolate.interp1d(ylst0, cllst0, kind='cubic', fill_value="extrapolate")
    cd_int_0 = sp.interpolate.interp1d(ylst0, cdlst0, kind='cubic', fill_value="extrapolate")
    cm_int_0 = sp.interpolate.interp1d(ylst0, cmlst0, kind='cubic', fill_value="extrapolate")

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
    cl_int_10 = sp.interpolate.interp1d(ylst10, cllst10, kind='cubic', fill_value="extrapolate")
    cd_int_10 = sp.interpolate.interp1d(ylst10, cdlst10, kind='cubic', fill_value="extrapolate")
    cm_int_10 = sp.interpolate.interp1d(ylst10, cmlst10, kind='cubic', fill_value="extrapolate")

    cly = (cl_int_10(y)-cl_int_0(y))*aoa/10 + cl_int_0(y)
    LperSpan = cly*q*c(y)
    return LperSpan

def MperSpan1(y):
    n_ult = -1.5
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
    aoa =  (cL-cL0)/(cL10-cL0)*10
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
    #below takes y as parameter and yields the spanwise cl, cdi and cm
    cl_int_0 = sp.interpolate.interp1d(ylst0, cllst0, kind='cubic', fill_value="extrapolate")
    cd_int_0 = sp.interpolate.interp1d(ylst0, cdlst0, kind='cubic', fill_value="extrapolate")
    cm_int_0 = sp.interpolate.interp1d(ylst0, cmlst0, kind='cubic', fill_value="extrapolate")

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
    cl_int_10 = sp.interpolate.interp1d(ylst10, cllst10, kind='cubic', fill_value="extrapolate")
    cd_int_10 = sp.interpolate.interp1d(ylst10, cdlst10, kind='cubic', fill_value="extrapolate")
    cm_int_10 = sp.interpolate.interp1d(ylst10, cmlst10, kind='cubic', fill_value="extrapolate")

    cmy = (cm_int_10(y)-cm_int_0(y))*aoa/10 + cm_int_0(y)
    MperSpan = cmy*q*c(y)*c(y)
    return MperSpan
