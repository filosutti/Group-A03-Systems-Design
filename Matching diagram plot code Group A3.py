import math
import numpy as np
import matplotlib.pyplot as plt

from tpw1_ROC import tpw1_function #Rate of climb function
from LFL_tpw import LandFieldTPW #Include which graph of the mathching diagram this is
from cruise_speed_function import cruise_speed_function #Cruise speed 
from minspeed import minSpeed #Include which graph of the mathching diagram this is
from CS25119 import CS25_119 #Include which graph of the mathching diagram this is
from function_file_name import tpw6_function #Include which graph of the mathching diagram this is
from function_file_name import tpw7_function #Include which graph of the mathching diagram this is
from function_file_name import tpw8_function #Include which graph of the mathching diagram this is

wps = 100 #initialise wing loading
tpw1lst = []
cruisespeedlst = []
LandingFieldLST = []
minspeedLST = []
CS25_119_LST = []
tpw6lst = []
tpw7lst = []
tpw8lst = []

wpslst = []

while(wps < 9000):
    tpw1lst.append(tpw1_function(wps))
    cruisespeedlst.append(cruise_speed_function(wps))
    LandingFieldLST.append(LandFieldTPW(wps))
    minspeedLST.append(minSpeed(wps))
    CS25_119_LST.append(CS25_119(wps))
    tpw6lst.append(tpw6(wps))
    tpw7lst.append(tpw7(wps))
    tpw8lst.append(tpw8(wps))
    wpslst.append(wps)
    wps = wps + 100

plt.plot(wpslst, tpw1lst, label = 'tpw1lst')
plt.plot(wpslst, cruisespeedlst, label = 'Cruise Speed Requirement')
plt.plot(wpslst, LandingFieldLST, label = 'Landing Field Requirement')
plt.plot(wpslst, minspeedLST, label = 'Minimum Speed Requirement')
plt.plot(wpslst, CS25_119_LST, label = 'CS25-119 Requirement')
plt.plot(wpslst, tpw6lst, label = 'tpw6lst')
plt.plot(wpslst, tpw7lst, label = 'tpw7lst')
plt.plot(wpslst, tpw8lst, label = 'tpw8lst')


#Design point selection
selected_wps = None
selected_tpw = None
plt.plot(selected_wps, selected_tpw, 'ro')

plt.xlabel('W/S - N/m2')
plt.ylabel('T/W - N/N')
plt.legend()
plt.title('Matching Diagram')
plt.show()