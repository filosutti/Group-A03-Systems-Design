from TL import c
import numpy as np 
import scipy as sp
from scipy import interpolate
from compressivestrength_and_otherfunctions import calculate_Ixx
from bendingdiagrampositiveload import M_pos_load
from Supremely_Ultimate_Julian_code_4 import inertia_calculation

#general geometry and constant parameters
wingspan = 23.78    #[m]
E = 72.4e9          #[Pa]
poratio = 0.33


    


# using loaded edges clamped so the dotted line 
# For test case C as it is the most conservative case

def k_c_value(a_b_value):
    # case C simply supported loaded edges
    a_b1 = [0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.45 ]
    k_c1 = [8.50, 8.00, 7.00, 6.00, 5.40, 5.00, 4.60, 4.40, 4.20, 4.10, 4.05, 4.00, 4.00, 4.05, 4.10, 4.20, 4.22, 4.25, 4.28, 4.30, 4.40 ]

    a_b2 = [1.45, 1.50, 1.55, 1.60, 1.65, 1.70, 1.75, 1.80, 1.85, 1.90, 1.95, 2.00, 2.25, 2.40, 2.50]
    k_c2 = [4.40, 4.30, 4.28, 4.25, 4.23, 4.20, 4.15, 4.13, 4.10, 4.05, 4.03, 4.00, 4.00, 4.10, 4.20]

    a_b3 = [2.50, 2.60, 2.75, 3.00, 3.25, 3.40, 3.50]
    k_c3 = [4.20, 4.10, 4.00, 4.00, 4.00, 4.05, 4.10]

    if 0.4 <= a_b_value <= 1.45:
        f = sp.interpolate.interp1d(a_b1, k_c1, kind = "cubic", fill_value = "extrapolate")
    
    elif 1.45 < a_b_value <= 2.50: 
        f = sp.interpolate.interp1d(a_b2, k_c2, kind = "cubic", fill_value = "extrapolate")
    
    elif 2.5 < a_b_value <= 3.50:
        f = sp.interpolate.interp1d(a_b3, k_c3, kind = "cubic", fill_value = "extrapolate")
    elif 3.5 < a_b_value: 
        return 4.0
    else: 
        raise ValueError("a/b value out of range")
    
    return f(a_b_value)

#here we import Ixx function
#NOTE: z is the position of a certain chord length, spanwise, inconsistent with what we re using elsewhere so we keep here only
y = 0 #at root 
I_xx, _, _, J = inertia_calculation(y)

#here we import Mx function from Julian
Mx = M_pos_load(y)


def crit_buckling_stress(nr_ribs, case):
    crit_stres = []
    if(case == 1):
        #Wing box design 1 geometry below
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
        z = 0.0573 * c(y)
        our_sigma = Mx * z / Ixx
        margin_of_safety.append(crit_stres/our_sigma)
    return margin_of_safety



