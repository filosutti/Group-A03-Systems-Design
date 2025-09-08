#Import
import math
import numpy as np

#----------------------------------------------------------------------------------------------------------------
#assumptions
massratioL = 0.925
gamma = 1.4
m = 0.77       #mach number
h_cruise = 10675 #metres
t_cruise = 218.76  #kelvin
p_cruise = 23809.88  #pascals
rho_cruise = 0.37923 #kg/m3 
ψ = 0.0075  # lift-dependent parasite drag parameter taken from adsee manual
φ = 0.97    #span efficiency factor assumed as above

h_ROC = 7400  #altitude for ROC requirement for similar mission aircraft data from prev year adsee spreadsheet
t_h_ROC = 240.05  #kelvin
p_h_ROC = 38780.84  #pascals
rho_h_ROC = 0.5629  #kg/m3
mass_frac_ROC = 0.95  #mass fraction for ROC, taken from similar aircraft data from prev year adsee spreadsheet
c = 12  #m/s

#--------------------------------------------------------
#Constants
g = 9.81

#--------------------------------------------------------
#Requirements
PLreq = 9302 #Payload (kg)
TOreq = 1296 #Takeoff (m)
LDreq = 1210 #Landing (m)
CRreq = 0.77 #Cruise (Mach)
Vcr_TAS = 228.332
Vcr_EAS = 127.104
R_des = 2019

#--------------------------------------------------------
#Class I weight estimation
MTOM = 38939.25
OEM = 22694.2
Mp = 9302
MF = MTOM - OEM - Mp 
ef = 44000000 
R_div = 250  #?

#--------------------------------------------------------
#PW1519G
ThrustPerEngine = 88 #kN
TSFC = 14 #g/(kNs)
njf = 0.371
BPR = 12

#--------------------------------------------------------
#wing
AR = 9
L = g
cf = 0.0027
SwetpS = 6
CLmax_cruise = 1.5
CLmax_Takeoff = 1.9
CLmax_Landing = 2.3
V_stall_requirement = 1
V_appro = 1.23 * V_stall_requirement
Cd0 = cf*SwetpS
Cd = 2*Cd0
nj = (Vcr_TAS/(TSFC/1000000))/ef


#--------------------------------------------------------
#Stats


#----------------------------------------------------------------------------------------------------------------
#Code


#--------------------------------------------------------
#Minimum speed formula



#--------------------------------------------------------
#Landing field Length formula



#--------------------------------------------------------
#Cruise speed formula



#--------------------------------------------------------
#Climb rate formula 



#--------------------------------------------------------
#Climb gradient requirements formulas



#--------------------------------------------------------
#Take-off field length formula
