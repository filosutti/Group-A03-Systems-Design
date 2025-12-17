from TL import c
import numpy as np 
import scipy as sp
from scipy import interpolate
from compressivestrength_and_otherfunctions import calculate_Ixx
from bendingdiagrampositiveload import M_pos_load
from Supremely_Ultimate_Julian_code_4 import inertia_calculation
from Spacing_Functions import rib_places
import matplotlib.pyplot as plt

#general geometry and constant parameters
wingspan = 23.78    #[m]
E = 72.4e9          #[Pa]
poratio = 0.33


#------------------------------------------------
#Run designs here by changing the 3 params below:
#------------------------------------------------

nr_ribs = 10
case = 3
initial_spacing = 1

#------------------------------------------------



# For test case C as it is the most conservative case
def k_c_value(a_b_value):
    # case C simply supported loaded edges
    a_b1 = [0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.45 ]
    k_c1 = [8.50, 8.00, 7.00, 6.00, 5.40, 5.00, 4.60, 4.40, 4.20, 4.10, 4.05, 4.00, 4.00, 4.05, 4.10, 4.17, 4.20, 4.25, 4.28, 4.33, 4.40 ]

    a_b2 = [1.45, 1.50, 1.55, 1.60, 1.65, 1.70, 1.75, 1.80, 1.85, 1.90, 1.95, 2.00, 2.25, 2.40, 2.50]
    k_c2 = [4.40, 4.30, 4.28, 4.25, 4.23, 4.20, 4.15, 4.13, 4.10, 4.05, 4.03, 4.00, 4.00, 4.10, 4.20]

    a_b3 = [2.50, 2.60, 2.75, 3.00, 3.25, 3.40, 3.50]
    k_c3 = [4.20, 4.10, 4.00, 4.00, 4.00, 4.05, 4.10]

    if 0.4 <= a_b_value <= 1.45:
        f = sp.interpolate.interp1d(a_b1, k_c1, kind = "quadratic", fill_value = "extrapolate")
    
    elif 1.45 < a_b_value <= 2.50: 
        f = sp.interpolate.interp1d(a_b2, k_c2, kind = "quadratic", fill_value = "extrapolate")
    
    elif 2.5 < a_b_value <= 3.50:
        f = sp.interpolate.interp1d(a_b3, k_c3, kind = "quadratic", fill_value = "extrapolate")
    elif 3.5 < a_b_value: 
        return np.interp(a_b_value, [3.5, 4, 1000], [4.1, 4.02, 4])
    else: 
        raise ValueError("a/b value out of range")
    
    return f(a_b_value)

#here we import Ixx function
#NOTE: z is the position of a certain chord length, spanwise, inconsistent with what we re using elsewhere so we keep here only


#function for equal spacing below:

def crit_buckling_stress1(nr_ribs, case):
    margin_of_safety1 = []
    if(case == 1):
        #Wing box design 1 geometry below
        t_skin = 6/1000      #[m]
        n_stringers = 12
    elif(case == 2):
        #Wing box design 2 geometry below
        t_skin = 6/1000      #[m]
        n_stringers = 6
    elif(case == 3):
        #Wing box design 3 geometry below
        t_skin = 12/1000        #[m]
        n_stringers = 6
    else:
        print("The code works :)") 
    i = 0
    a = wingspan/(2*(nr_ribs - 1))
    while (i+1<nr_ribs):
        y = a*i
        Mx = M_pos_load(y)
        I_xx, _, _, J = inertia_calculation(y)
        b = (c(y)*0.5 + c(y + a)*0.5)/(n_stringers + 1)/2
        t = t_skin
        crit_stres = np.pi*np.pi*k_c_value(a/b)*E/(12*(1-poratio*poratio))*(t/b)*(t/b)
        z = - 0.0573 * c(y)
        our_sigma = Mx * z / I_xx
        margin_of_safety1.append(crit_stres/our_sigma)
        i = i+1
    return margin_of_safety1

#function for linear spacing diff below:

def crit_buckling_stress2(nr_ribs, case, initial_spacing):
    ylst2, spacings = rib_places(initial_spacing, 11.89, nr_ribs)
    print(ylst2)
    margin_of_safety2 = []
    if(case == 1):
        #Wing box design 1 geometry below
        t_skin = 6/1000      #[m]
        n_stringers = 12
    elif(case == 2):
        #Wing box design 2 geometry below
        t_skin = 6/1000      #[m]
        n_stringers = 6
    elif(case == 3):
        #Wing box design 3 geometry below
        t_skin = 12/1000        #[m]
        n_stringers = 6
    else:
        print("The code works :)") 
    i = 0
    while (i+1<nr_ribs):
        y = ylst2[i]
        a = spacings[i]
        Mx = M_pos_load(y)
        I_xx, _, _, J = inertia_calculation(y)
        b = (c(y)*0.5 + c(y + a)*0.5)/(n_stringers + 1)/2
        t = t_skin
        crit_stres = (np.pi*np.pi*k_c_value(a/b)*E/(12*(1-poratio*poratio))*(t/b)*(t/b))
        z = - 0.0573 * c(y)
        our_sigma = Mx * z / I_xx
        margin_of_safety2.append(crit_stres/our_sigma)
        i = i+1
    return margin_of_safety2

a_eq = wingspan / (2 * (nr_ribs - 1))
ylst1 = np.array([a_eq * i for i in range(nr_ribs - 1)])
mos1 = crit_buckling_stress1(nr_ribs, case)

ylst2, _ = rib_places(initial_spacing, wingspan/2, nr_ribs)
ylst2 = ylst2[:-1]   # last rib has no following spacing
mos2 = crit_buckling_stress2(nr_ribs, case, initial_spacing)

print(ylst2)
plt.figure()
plt.plot(ylst1, mos1, marker='o', label='Equal spacing')
plt.plot(ylst2, mos2, marker='s', label='Linear spacing')

plt.xlabel('Spanwise location y [m]')
plt.ylabel('Margin of Safety')
plt.title('Buckling Margin of Safety Along the Span')
plt.grid(True)
plt.legend()
plt.show()