import scipy 
import numpy 
from matplotlib import pyplot as plt


#Constants 
#-------------------------------------------------------------------------------------
g = 9.81
n_pos = 2.5
n_neg = -1
winghalfspan = 11.89 #m
wingweight = 909.447 #kg

#-------------------------------------------------------------------------------------
#choose whether n is pos or neg
n_choose = n_pos
#-------------------------------------------------------------------------------------


#Define Point Loads
#-------------------------------------------------------------------------------------
W_engine_NOLOAD = 2177.243*g

def Heaviside(x, x0):
    return 1.0 if x >= x0 else 0.0

# Distributed Loads
#-------------------------------------------------------------------------------------
def LiftDistribution(x, n):
    return (x)*n

def WeightDistribution(x,n):
    return ((7*x)-821.693393608074)*n

def FuelDistribution(x):
    return x

def w(x):
    return LiftDistribution(x,n_choose) - WeightDistribution(x,n_choose) - FuelDistribution(x)


#Define Point Loads
#-------------------------------------------------------------------------------------
def w(x):
    return LiftDistribution(x,n_choose) - WeightDistribution(x,n_choose) - FuelDistribution(x) - W_engine_NOLOAD



ShearEstimate, error1 = scipy.integrate.quad(w, 0, winghalfspan)
print(ShearEstimate)

