import math
import numpy as np
import matplotlib.pyplot as plt

from tpw1_ROC import tpw1_function #Rate of climb function
from LFL_tpw import LandFieldTPW 
from cruise_speed_function import cruise_speed_function #Cruise speed 
from minspeed import minSpeed 
from CS25119 import CS25_119 
from CS25_121a import CS25_121a_function 
from CS25_121b import CS121b_function 
from function_file_name import tpw8_function 
from function_file_name import tpw8_function 
from function_file_name import tpw8_function 


#VARIABLES & CONSTANTS
#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------

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
mass_frac_cruise = 0.90


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

#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------


wps = 100 #initialise wing loading
cruisespeedlst = []
LandingFieldLST = []
minspeedLST = []
CS25_119_LST = []
CS25_121A_LST = []
CS25_121B_LST = []
tpw7lst = []
tpw8lst = []

wpslst = []

while(wps < 9000):
    cruisespeedlst.append(cruise_speed_function(wps))
    LandingFieldLST.append(LandFieldTPW(wps))
    minspeedLST.append(minSpeed(wps, massfraction, V_appro))
    CS25_119_LST.append(CS25_119(wps))
    CS25_121A_LST.append(CS25_121a_function(wps))
    CS25_121B_LST.append(CS121b_function(wps))
    tpw8lst.append(tpw8(wps))
    wpslst.append(wps)
    wps = wps + 100

plt.plot(wpslst, cruisespeedlst, label = 'Cruise Speed Requirement')
plt.plot(wpslst, LandingFieldLST, label = 'Landing Field Requirement')
plt.plot(wpslst, minspeedLST, label = 'Minimum Speed Requirement')
plt.plot(wpslst, CS25_119_LST, label = 'CS25-119 Requirement')
plt.plot(wpslst, CS25_121A_LST, label = 'CS25-121a Requirement')
plt.plot(wpslst, CS25_121B_LST, label = 'CS25-121b Requirement')
plt.plot(wpslst, tpw8lst, label = 'CS25-121c Requirement')
plt.plot(wpslst, tpw9lst, label = 'CS25-121d Requirement')


#Design point selection
selected_wps = None
selected_tpw = None
plt.plot(selected_wps, selected_tpw, 'ro')

plt.xlabel('W/S - N/m2')
plt.ylabel('T/W - N/N')
plt.legend()
plt.title('Matching Diagram')
plt.show()