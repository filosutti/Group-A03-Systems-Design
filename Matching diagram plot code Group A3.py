import math
import numpy as np
import matplotlib.pyplot as plt

from function_file_name import tpw1
from function_file_name import tpw2
from function_file_name import tpw3
from function_file_name import tpw4
from function_file_name import tpw5
from function_file_name import tpw6
from function_file_name import tpw7
from function_file_name import tpw8

wps = 0 #wing loading
tpw1lst = []
tpw2lst = []
tpw3lst = []
tpw4lst = []
tpw5lst = []
tpw6lst = []
tpw7lst = []
tpw8lst = []
wpslst = []

while(wps < 9000):
    tpw1lst.append(tpw1(wps))
    tpw2lst.append(tpw2(wps))
    tpw3lst.append(tpw3(wps))
    tpw4lst.append(tpw4(wps))
    tpw5lst.append(tpw5(wps))
    tpw6lst.append(tpw6(wps))
    tpw7lst.append(tpw7(wps))
    tpw8lst.append(tpw8(wps))
    wpslst.append(wps)
    wps = wps + 100

plt.plot(wpslst, tpw1lst, label = 'tpw1lst')
plt.plot(wpslst, tpw2lst, label = 'tpw2lst')
plt.plot(wpslst, tpw3lst, label = 'tpw3lst')
plt.plot(wpslst, tpw4lst, label = 'tpw4lst')
plt.plot(wpslst, tpw5lst, label = 'tpw5lst')
plt.plot(wpslst, tpw6lst, label = 'tpw6lst')
plt.plot(wpslst, tpw7lst, label = 'tpw7lst')
plt.plot(wpslst, tpw8lst, label = 'tpw8lst')


#Design point selection
selected_wps = 
selected_tpw = 
plt.plot(selected_wps, selected_tpw, 'ro')

plt.xlabel('W/S - N/m2')
plt.ylabel('T/W - N/N')
plt.legend()
plt.title('Matching Diagram')
plt.show()