from TL import c
import numpy as np 
import scipy as sp
from scipy import interpolate
#general geometry and constant parameters
wingspan = 23.78    #[m]
E = 72.4e9          #[Pa]
poratio = 0.33
#Wing box design 1 geometry below



# using loaded edges clamped so the dotted line 
# For test case.... (don't know which case we're using yet)

def k_c_value(a_b_value):
    # case A
    a_b = [0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.60,0.70,0.80,0.90,1.00,1.10,1.20,1.30,1.40,1.50,1.70,2.00,2.50,
    3.00,3.50,4.00,4.50,5.00]
    k_c = [15.3,14.0,12.7,11.6,10.7,10.1,9.6,8.8,8.2,7.85,7.55,7.30,7.15,7.05,6.95,6.85,6.78,6.70,6.55,6.42,
    6.34,6.27,6.22,6.18,6.15]

    f = sp.interpolate.interp1d(a_b, k_c, kind = "cubic", fill_value = "extrapolate")
    return f(a_b_value)


def crit_buckling_stress(nr_ribs, case):
    crit_stres = []
    if(case == 1):
        t_skin = 1.5/1000      #[m]
        t_spar = 1.5/1000      #[m]
        t_stringer = 1/1000    #[m] 
        w_stringer = 15/1000   #[m]
        n_stringers = 12
    elif(case == 2):
        #Wing box design 2 geometry below
        t_skin = 1.5/1000      #[m]
        t_spar = 1.5/1000      #[m]
        t_stringer = 2/1000    #[m] 
        w_stringer = 20/1000   #[m]
        n_stringers = 6
    elif(case == 3):  
        #Wing box design 3 geometry below
        t_skin = 3/1000        #[m]
        t_spar = 3/1000        #[m]
        t_stringer = 1/1000    #[m] 
        w_stringer = 15/1000   #[m]
        n_stringers = 6
    else:
        print("The code works :)") 
    i = 0
    a = wingspan/(2*(n_stringers - 1))
    while (i+1<nr_ribs):
        i = i+1
        y = a*i
        b = c(y)*0.5/(n_stringers + 1)
        t = t_skin * c(y)
        crit_stres.append(np.pi*np.pi*6*E/(12*(1-poratio*poratio))*(t/b)*(t/b))
    return crit_stres
print(crit_buckling_stress(8, 1))