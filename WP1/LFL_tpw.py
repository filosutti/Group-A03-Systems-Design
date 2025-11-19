#Import
import math

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
CRreq = 0.77 #Cruise (Mach)
Vcr_TAS = 228.332
Vcr_EAS = 127.104
R_des = 2019

#--------------------------------------------------------
#Class I weight estimation
MTOM = 32142.392908426657
OEM = 19285.4357
Mass_payload = 9302

Mass_fuel = MTOM - OEM - Mass_payload 

ef = 44000000 
R_div = 250  #?

#--------------------------------------------------------
#PW1519G
ThrustPerEngine = 88 #kN
TSFC = 11.3 #g/(kNs)
njf = 0.46
BPR = 12

#--------------------------------------------------------
#wing
AR = 9
L = g
cf = 0.0027
SwetpS = 6
CLmax_cruise = 1.5
CLmax_Takeoff = 1.9

V_stall_requirement = 1
V_appro = 1.23 * V_stall_requirement
Cd0 = cf*SwetpS
Cd = 2*Cd0
nj = (Vcr_TAS/(TSFC/1000000))/ef



#----------------------------------------------------------------------------------------------------------------
#Code
<<<<<<< Updated upstream
<<<<<<< Updated upstream
def LandFieldTPW(wps):
=======

def LandFieldTPW(wps,CLmax_Landing):
>>>>>>> Stashed changes
=======

def LandFieldTPW(wps,CLmax_Landing):
>>>>>>> Stashed changes
    beta = 0.84
    rho0 = 1.225226 #[kg/m^3]
    C_LFL = 0.37 #[s^2/m]
    LandingFieldLength = 1210

    #----------------------------------------------------------------------------------------------------------------
    #Landing Field Length formulae
    
    Landing_Field_TPW = (1/beta) * (LandingFieldLength/C_LFL) * (0.5 * rho0 * CLmax_Landing)
    
    return Landing_Field_TPW



