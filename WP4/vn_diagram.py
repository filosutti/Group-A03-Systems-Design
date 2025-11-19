#CODE
import matplotlib.pyplot as plt
from Katerina_code import *


m_maxto=27719.34119
n_max=max((2.1+24000/(9.80665*m_maxto*0.2248+10000)), 2.5)
n_ult=1.5*n_max
n_min=-1
n_ult2=n_min*1.5

def VEAS(v, h):
    T0, P0, Rho0, a0=ISA(0)
    T, P, Rho, a=ISA(h)
    v_eas=v*(Rho/Rho0)
    return(v_eas)
    
m=27719

v_list=[0]
n_list=[0]
V=0
V_S0ap, V_S0to, V_S1, V_A, V_D, V_F1, V_F2, V_F3, V_F=nvdiagram(0, m, n_max)
while V<V_S1*(n_max)**0.5:
    V=min(V+1, V_S1*(n_max)**0.5)
    n=(V/V_S1)**2
    v_list.append(V)
    n_list.append(n)
while V_S1*(n_max)**0.5<=V<V_D:
    n=n_max
    V=max(V+1, V_D)
    v_list.append(V)
    n_list.append(n)

while 0<n<=n_max:
    V=V
    n=int(10*(n-0.1))/10
    v_list.append(V)
    n_list.append(n)
while V_c<V<=V_D:
    V=V-1
    n=(-n_min/(V_D-V_c))*V+n_min*V_D/(V_D-V_c)
    v_list.append(V)
    n_list.append(n)
while V_S1<V<=V_c:
    V=V-1
    n=n_min
    v_list.append(V)
    n_list.append(n)
while 0<V<=V_S1*(n_max)**0.5:
    V=V-1
    n=-(V/V_S1)**2
    v_list.append(V)
    n_list.append(n)

    
plt.figure()
plt.plot(v_list, n_list)
plt.xlabel("Equivalent Airspeed V (kts or m/s)")
plt.ylabel("Load Factor n")
plt.title("V–n Diagram")
plt.grid(True)
plt.show()


print(V_c, V_S0ap, V_S0to, V_S1, V_A, V_D, V_F1, V_F2, V_F3, V_F)
    
    
    
    
