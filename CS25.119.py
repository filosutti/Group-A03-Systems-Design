import math
import numpy as np

BPR=12
c=3.2 #climb gradient
AR=9
psi=0.0075
phi=0.97
flap_deflection=35 #degrees
cf=0.0027
SwetpS=6
lgd0=0.0175 #landing gear drag coefficient
gamma=1.4
R=287
T=288.15
P=101325
MR=1 #mass ratio
Cl=2.3

e0=1/(np.pi*AR*psi+1/phi) #original oswald
e=e0+0.0026*flap_deflection #New oswald with flaps
cd00=cf*SwetpS #original cd0
cd0=cd00+lgd0+0.0013*flap_deflection #cd0 with lg and flaps

def twcs119(wps):
    V=(2*wps*R*T/(P*2.3))**0.5 #Velocity at landing cl
    M=V/((gamma*R*T)**0.5)
    Tt=T*(1+(gamma-1)*0.5*(M**2)) #total temp
    pt=P*((1+(gamma-1)*0.5*M**2)**(gamma/(gamma-1))) #total press
    st=pt/P 
    tht=Tt/T
    at=st*(1-(0.43+0.014*BPR)*(M**(0.5))) #lapse rate
    t_w=(MR/at)*(c/100+2*(cd0/(np.pi*AR*e))**(0.5))
    return(t_w)





