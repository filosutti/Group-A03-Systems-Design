#CODE
h_cruise=10668
M_cr=0.77
CL_maxcr=1.56
CL_maxto=2.4344
CL_maxap=2.653
    
def ISA(h):
    T=288.15-0.0065*h
    P=101325*(T/288.15)**(9.80665/(0.0065*287))
    Rho=P/(287*T)
    a=(1.4*287*T)**0.5
    return(T, P, Rho, a)

def Veq(CL, m, h):
    T, P, Rho, a=ISA(h)
    v=((2*9.80665*m)/(Rho*CL*62.8299727939332))**0.5
    return(v)

def VEAS(v, h):
    T0, P0, Rho0, a0=ISA(0)
    T, P, Rho, a=ISA(h)
    v_eas=v*(Rho/Rho0)
    return(v_eas)
    

def nvdiagram(h, m):
    a_cr=ISA(10668)
    V_cr=M_cr*a_cr
    V_S0ap=Veq(CL_maxap, m, h)
    V_S0to=Veq(CL_maxto, m, h)
    V_S1=Veq(CL_maxcr, m, h)
    return (V_S0ap, V_S0to, V_S1)

m=27719

print(Veq(0.433, m, 10668))
    
