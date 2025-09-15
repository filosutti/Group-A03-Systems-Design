#Import
import math
import numpy as np

#----------------------------------------------------------------------------------------------------------------
#assumptions
massratioL = 0.925
gamma = 1.4
m = 0.77       #mach number
h_cruise = 10675 #metres
t_cruise = 214.53  #kelvin
p_cruise = 21485.9  #pascals
rho_cruise = 0.3489 #kg/m3 
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
MTOM = 32142.3929
OEM = 19285.4357
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
e = 1/(np.pi*AR*ψ + 1/φ)
mass_frac_cruise = 0.90



def cruise_speed_function(wps):
    α = p_cruise/101325*(1-(0.43+0.014*BPR)*np.sqrt(m))  #thrust lapse rate
    tpw = (mass_frac_cruise / α)*(((Cd0*0.5*rho_cruise*Vcr_TAS**2) / (0.95*wps))+((0.95*wps)/(np.pi*AR*e*0.5*rho_cruise*Vcr_TAS**2)))
    return tpw

      