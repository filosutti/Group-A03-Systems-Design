import scipy 
import numpy as np
from matplotlib import pyplot as plt
from TL import LperSpan1, LperSpan0



#Constants 
#-------------------------------------------------------------------------------------
g = 9.81
winghalfspan = 11.89 #m
wingweight = 909.447 #kg


#Define Point Loads
#-------------------------------------------------------------------------------------
W_engine_NOLOAD = 2177.243*g
x_engine = 3.75 #metres

def Heaviside(x, x0):
    return 1.0 if x >= x0 else 0.0

# Distributed Loads
#-------------------------------------------------------------------------------------
def LiftDistribution(x):
    return LperSpan0(x)

def WeightDistribution(x):
    return -10*x+809.9966

def FuelDistribution(x):
    return -10*x+4582.681836


#Finding Root Internal reaction shear 
def V0_calc():
    Fuel, FuelError = scipy.integrate.quad(FuelDistribution, 0, winghalfspan)
    Lift, LiftError = scipy.integrate.quad(LperSpan0, 0, winghalfspan)
    return - Fuel - wingweight * g - W_engine_NOLOAD + Lift 

V0 = V0_calc()


#Distributed Loading
#-------------------------------------------------------------------------------------
def w(x):
    return  - LiftDistribution(x) + WeightDistribution(x) + FuelDistribution(x) 

#Shear
#-------------------------------------------------------------------------------------
def Shear(x):
    ShearIntegral, ShearError = scipy.integrate.quad(w, x, winghalfspan)
    Engine_PointLoad_Shear = W_engine_NOLOAD * (1-Heaviside(x,x_engine))
    Root_Internal_Shear = V0 * (1-Heaviside(x,0))
    return - ShearIntegral - Engine_PointLoad_Shear + Root_Internal_Shear


xs = np.linspace(0,winghalfspan,200) #200 datapoints 
Ss = [Shear(x)/10**3 for x in xs]

xs = np.insert(xs, 0, 0.0)
Ss = np.insert(Ss, 0, 0.0)

S_engine = float(np.interp(x_engine, xs, Ss))

plt.figure(figsize=(10, 6))

# Main shear curve (blue)
plt.plot(xs, Ss, label='Shear Force V(y) (Positive Load Factor)', color='blue')

# Engine vertical dotted line from axis to function
plt.plot([x_engine, x_engine],
         [0, S_engine],
         color='red', linestyle=':', label='Engine Location')

# Formatting
plt.title('Shear Force Distribution Along Wingspan (+3.75g Load Factor)')
plt.xlabel('Spanwise Location y (m)')
plt.ylabel('Shear Force V(y) [kN]')
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.legend()
plt.grid()
plt.show()

print(Shear(5))