#CODE
import matplotlib.pyplot as plt
import numpy as np
from Katerina_code import *


m_maxto=27719.34119
oem=14477
m_nofuel=oem+9302
n_max=max((2.1+24000/(9.80665*m_maxto*0.2248+10000)), 2.5)
n_ult=1.5*n_max
n_min=-1
n_ult2=n_min*1.5

def VEAS(v, h):
    T0, P0, Rho0, a0=ISA(0)
    T, P, Rho, a=ISA(h)
    v_eas=v*(Rho/Rho0)
    return(v_eas)

v_list=[0]
v1_list=[0]
n1_list=[0]
n_list=[0]
v2_list=[0]
n2_list=[0]
v3_list=[0]
n3_list=[0]
V=0
V1 = 0
V2=0
V_S0ap, V_S0to, V_S1, V_A, V_F1, V_F2, V_F3, V_F=nvdiagram(0, oem, n_max)
V_int=(2*V_S1**2)**0.5
while V<V_A:
    V=min(V+1, V_A)
    n=(V/V_S1)**2
    v_list.append(V)
    n_list.append(n)
while V_A<=V<V_D:
    n=n_max
    V=min(V+1, V_D)
    v_list.append(V)
    n_list.append(n)

while 0<n<=n_max:
    n = round(n - 0.1, 2)
    v_list.append(V)
    n_list.append(n)
while V_C<V<=V_D:
    V=V-1
    n=max((-n_min/(V_D-V_C))*V+n_min*V_D/(V_D-V_C), n_min)
    v_list.append(V)
    n_list.append(n)
while V_S1<V<=V_C:
    V=V-1
    n=n_min
    v_list.append(V)
    n_list.append(n)
while 0<V<=V_S1:
    V=max(V-1, 0)
    n=-(V/V_S1)**2
    v_list.append(V)
    n_list.append(n)

v_arr = np.array(v_list)
n_arr = np.array(n_list)

while V1 < V_F and V1<V_int:
    V1 = min(V1 + 1, V_F, V_int)
    n1 = min((V1 / V_S0ap)**2, 2)

    v1_list.append(V1)
    n1_list.append(n1)

while V2 < V_F and V2<V_int:
    V2 = min(V2 + 1, V_F, V_int)
    n2 = min((V2 / V_S0to)**2, 2)

    v2_list.append(V2)
    n2_list.append(n2)
        
"""
plt.figure(figsize=(10,6))
plt.plot(v_list, n_list, label="No Flaps")
plt.plot(v1_list, n1_list, label="Landing Flaps")
plt.plot(v2_list, n2_list, label="Take-off Flaps")
plt.xlabel("Equivalent Airspeed V (m/s)")
plt.ylabel("Load Factor n [-]")
plt.title("V–n Diagram Sea-Level No Fuel Weight")
plt.grid(True)
plt.legend()
plt.show()

print(V_A)
print(V_C)
print(V_D)
print(V_S1)
    
    
    
"""
