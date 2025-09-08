import math
import numpy as np

Cl_landing=2.3
BPR=12
c=3.2
AR=9
psi=0.0075
phi=0.97
flap_deflection=35
cf=0.0027
SwetpS=6
lgd0=0.0175
gamma=1.4
R=287
T=288.15
P=101325
MR=1
Cl=2.3

e0=1/(np.pi*AR*psi+1/phi)
e=e0+0.0026*flap_deflection
cd00=cf*SwetpS
cd0=cd00+lgd0+0.0013*flap_deflection

def twcs119(wps):
    V=(2*wps*R*T/(P*2.3))**0.5
    M=V/((gamma*R*T)**0.5)
    Tt=T*(1+(gamma-1)*0.5*(M**2))
    pt=P*((1+(gamma-1)*0.5*M**2)**(gamma/(gamma-1)))
    st=pt/P
    tht=Tt/T
    at=st*(1-(0.43+0.014*BPR)*(M**(0.5)))
    t_w=(MR/at)*(c/100+2*(cd0/(np.pi*AR*e))**(0.5))
    return(t_w)





