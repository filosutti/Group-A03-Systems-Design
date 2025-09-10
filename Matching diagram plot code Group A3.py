import math
import numpy as np
import matplotlib.pyplot as plt

from tpw1_ROC import tpw1_function #Rate of climb function
from LFL_tpw import LandFieldTPW 
from cruise_speed_function import cruise_speed_function #Cruise speed 
from minspeed import minSpeed 
from CS25119 import CS25_119 
from CS25_121a import CS25_121a_function 
from CS25_121b import CS25121B_func 
from CS25_121c import CS25_121c_function
from CS25_121d import CS25_121d_function
from TO_req import TOF_req


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
MTOM = 32142.392
OEM = 19285.435
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
V_stall_requirement = 57
V_appro = 1.23 * V_stall_requirement
Cd0 = cf*SwetpS
Cd = 2*Cd0
nj = (Vcr_TAS/(TSFC/1000000))/ef

#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------


wps = 200 #initialise wing loading
ROC_LST = []
cruisespeedlst = []
LandingFieldLST = []
minspeedLST = []
CS25_119_LST = []
CS25_121A_LST = []
CS25_121B_LST = []
CS25_121C_LST = []
CS25_121D_LST = []
TO_LST = []
lfllst = []
wpslst = []

i = 0.1
while(i<9):
    lfllst.append(i)
    i = i+0.1

while(wps < 9200):

    try:
        cruisespeedlst.append(cruise_speed_function(wps))
    except ZeroDivisionError:
        cruisespeedlst.append(0)
    try:
        LandingFieldLST.append(LandFieldTPW(wps))
    except ZeroDivisionError:
        LandingFieldLST.append(0)
    try:
        minspeedLST.append(minSpeed(wps, V_appro))
    except ZeroDivisionError:
        minspeedLST.append(0)
    try:
        CS25_119_LST.append(CS25_119(wps))
    except ZeroDivisionError:
        CS25_119_LST.append(0)
    try:
        CS25_121A_LST.append(CS25_121a_function(wps))
    except ZeroDivisionError:
        CS25_121A_LST.append(0)
    try:
        CS25_121B_LST.append(CS25121B_func(wps))
    except ZeroDivisionError:
        CS25_121B_LST.append(0)
    try:
        CS25_121C_LST.append(CS25_121c_function(wps))
    except ZeroDivisionError:
        CS25_121C_LST.append(0)
    try:
        CS25_121D_LST.append(CS25_121d_function(wps))
    except ZeroDivisionError:
        CS25_121D_LST.append(0)
    try:
        TO_LST.append(TOF_req(wps))
    except ZeroDivisionError:
        TO_LST.append(0)
    try:
        ROC_LST.append(tpw1_function(wps))
    except ZeroDivisionError:
        ROC_LST.append(0)
    wpslst.append(wps)
    wps = wps + 100



plt.plot(wpslst, cruisespeedlst, label = 'Cruise Speed Requirement')
plt.plot(LandingFieldLST, lfllst, label = 'Landing Field Requirement')
plt.plot(minspeedLST, lfllst, label = 'Minimum Speed Requirement')
plt.plot(wpslst, CS25_119_LST, label = 'CS25-119 Requirement')
plt.plot(wpslst, CS25_121A_LST, label = 'CS25-121a Requirement')
plt.plot(wpslst, CS25_121B_LST, label = 'CS25-121b Requirement')
plt.plot(wpslst, CS25_121C_LST, label = 'CS25-121c Requirement')
plt.plot(wpslst, CS25_121D_LST, label = 'CS25-121d Requirement')
plt.plot(wpslst, TO_LST, label = 'TakeOff Requirement')
plt.plot(wpslst, ROC_LST, label = 'Climb Rate Requirement')

#--------------------------------------------------------------------------------
#DESIGN POINT
x_design =      #<<ENTER W/S for design point
y_design =      #<<ENTER T/W for design point
plt.scatter(x_design, y_design, color='red', marker='o', s=40)
plt.text(x_design + 30, y_design + 0.01, 'Fokker 70', color='red')

#Design points for reference aircrafts
# Fokker 70
x_f70 = 4187.873262
y_f70 = 0.312590861
plt.scatter(x_f70, y_f70, color='red', marker='*', s=50)
plt.text(x_f70 + 30, y_f70 + 0.01, 'Fokker 70', color='red')

# ARJ21-700 STD
x_ARJ21 = 4975.018783
y_ARJ21 = 0.381923208
plt.scatter(x_ARJ21, y_ARJ21, color='red', marker='*', s=50)
plt.text(x_ARJ21 + 30, y_ARJ21 + 0.01, 'ARJ21-700 STD', color='red')

# Embraer E 170
x_E170 = 5207.178218
y_E170 = 0.328944241
plt.scatter(x_E170, y_E170, color='red', marker='*', s=50)
plt.text(x_E170 - 160, y_E170 - 0.01, 'Embraer E 170', color='red')

# CRJ 700
x_CRJ700 = 4727.002691
y_CRJ700 = 0.367366812
plt.scatter(x_CRJ700, y_CRJ700, color='red', marker='*', s=50)
plt.text(x_CRJ700 + 30, y_CRJ700 + 0.01, 'CRJ 700', color='red')

# CRJ 900
x_CRJ900 = 5288.56962
y_CRJ900 = 0.343069322
plt.scatter(x_CRJ900, y_CRJ900, color='red', marker='*', s=50)
plt.text(x_CRJ900 + 30, y_CRJ900 + 0.01, 'CRJ 900', color='red')

# Avro RJ70
x_RJ70 = 4835.327426
y_RJ70 = 0.332824278
plt.scatter(x_RJ70, y_RJ70, color='red', marker='*', s=50)
plt.text(x_RJ70 + 30, y_RJ70 + 0.01, 'Avro RJ70', color='red')

# Avro RJ85
x_RJ85 = 5353.493402
y_RJ85 = 0.300610132
plt.scatter(x_RJ85, y_RJ85, color='red', marker='*', s=50)
plt.text(x_RJ85 + 30, y_RJ85 - 0.028, 'Avro RJ85', color='red')

# One-Eleven 475
x_111475 = 4577.317328
y_111475 = 0.254499928
plt.scatter(x_111475, y_111475, color='red', marker='*', s=50)
plt.text(x_111475 + 30, y_111475 + 0.01, 'One-Eleven 475', color='red')

#--------------------------------------------------------------------------------


#Design point selection
selected_wps = None
selected_tpw = None
#plt.plot(selected_wps, selected_tpw, 'ro')

plt.xlabel('W/S - N/m2')
plt.ylabel('T/W - N/N')
plt.legend()
plt.title('Matching Diagram')
plt.show()