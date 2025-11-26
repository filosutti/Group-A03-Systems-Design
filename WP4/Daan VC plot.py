import matplotlib.pyplot as plt
h_cruise=10668
def ISA(h):
    T=288.15-0.0065*h
    P=101325*(T/288.15)**(9.80665/(0.0065*287))
    Rho=P/(287*T)
    a=(1.4*287*T)**0.5
    return(T, P, Rho, a)

a_cruise = ISA(h_cruise)[3]

vc=127

def VEAS(v, h):
    T0, P0, Rho0, a0=ISA(0)
    T, P, Rho, a=ISA(h)
    v_eas=v*(Rho0/Rho)**0.5
    return(v_eas)
h=0
H=[]
M=[]
while h<10668:
    V=VEAS(vc, h)
    a1=ISA(h)[3]
    M1=V/a1
    H.append(h)
    M.append(M1)
    h=h+1


plt.figure(figsize=(10,6))
plt.plot(H, M)
plt.xlabel("Height (m)")
plt.ylabel("Mach Number of Vc [-]")
plt.title("Mach Number Design Cruise Speed against Height")
plt.grid(True)
plt.show()
    
