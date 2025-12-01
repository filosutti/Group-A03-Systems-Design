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
    return LperSpan1(x)

def WeightDistribution(x):
    return -10*x+809.9966

def FuelDistribution(x):
    return 10*x-9148.6175 


#Finding Root Internal reaction shear 
def V0_calc():
    Fuel, FuelError = scipy.integrate.quad(FuelDistribution, 0, winghalfspan)
    Lift, LiftError = scipy.integrate.quad(LperSpan0, 0, winghalfspan)
    return - Fuel - wingweight * g - W_engine_NOLOAD + Lift 

V0 = V0_calc()


#Distributed Loading
#-------------------------------------------------------------------------------------
def w(x):
    return - LiftDistribution(x) + WeightDistribution(x) + FuelDistribution(x) 

#Shear
#-------------------------------------------------------------------------------------
def Shear(x):
    ShearIntegral, ShearError = scipy.integrate.quad(w, x, winghalfspan)
    Engine_PointLoad_Shear = W_engine_NOLOAD * (1-Heaviside(x,x_engine))
    Root_Internal_Shear = V0 * (1-Heaviside(x,0))
    return - ShearIntegral - Engine_PointLoad_Shear + Root_Internal_Shear


xs = np.linspace(0,winghalfspan,200) #200 datapoints 
Ss = [Shear(x) for x in xs]
plt.figure(figsize=(10, 6))   # wider figure
plt.plot(xs, Ss)
plt.xlabel("Spanwise position x [m]")
plt.ylabel("Shear S(x) [N]")
plt.title("Shear Force with a NEGATIVE load factor")
plt.show()