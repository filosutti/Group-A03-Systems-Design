import math
import numpy as np

#assumptions
massratioL = 0.925
h_cruise = 10675   #metres
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

#Constants
g = 9.81

#Requirements
PLreq = 9302 #Payload (kg)
TOreq = 1296 #Takeoff (m)
LDreq = 1210 #Landing (m)
CRreq = 0.77 #Cruise (Mach)
Vcr_TAS = 228.332
Vcr_EAS = 127.104
R_des = 2019
#Class I weight estimation
MTOM = 38939.25
OEM = 22694.2
Mp = 9302
MF = MTOM - OEM - Mp 
ef = 44000000 
R_div = 250  #?
#wing
   #assumed
e = 1/(np.pi*AR*ψ + 1/φ)  #oswald eff factor
L = g
cf = 0.0027
SwetpS = 6
CLmax_cruise = 1.5
CLmax_Landing = 2.3
V_stall_requirement = 1
V_appro = 1.23 * V_stall_requirement
Cd0 = cf*SwetpS
Cd = 2*Cd0


#PW1519G
ThrustPerEngine = 88 #kN
TSFC = 11.3 #g/(kNs)
njf = 0.46



#------------------------------------


def CS25_121a_function(wps):

    AR = 9
    BPR = 12
    gamma = 1.4
    CLmax_Takeoff = 1.9
    delta_takeoff = 15 #degrees, maximum flap deflection for take off
    delta_landing_gear = 0.0175
    e_final = e + 0.0026*delta_takeoff  #equation 7.62
    Cd0_final = Cd0 + 0.0013*delta_takeoff + delta_landing_gear   #equation 7.63 and 7.64
    mach = 0.77
    
    αt = (1 + (gamma-1)/2*mach*mach)^(gamma/(gamma-1))*(1 - (0.43 + 0.014*BPR)*np.sqrt(mach)) #equation 7.37
    tpw = 2/αt*(2*np.sqrt(Cd0_final/np.pi/AR/e_final)+c/np.sqrt(wps*2/CLmax_Takeoff/1.225))
    
    return tpw
