#CODE
h_cruise=10668
M_cr=0.77
CL_maxcr=1.56
CL_maxto=2.4344
CL_maxap=2.653
m_maxto=27719.34119
n_max=max((2.1+24000/(9.80665*m_maxto*0.2248+10000)), 2.5)
n_min=-1
    
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

v_list=[0]
n_list=[0]
V=0
V_S1=25
V_D=200
V_F=160
while V<=V_S1*(n_max)**0.5:
    n=(V/V_S1)**2
    V=V+1
    v_list.append(V)
    n_list.append(n)
while V_S1*(n_max)**0.5<=V<V_D:
    n=n_max
    V=V+1
    v_list.append(V)
    n_list.append(n)

while 0<n<=n_max:
    V=V
    n=int(10*(n-0.1))/10
    v_list.append(V)
    n_list.append(n)
while V_F<V<=V_D:
    V=V-1
    n=(-n_min/(V_D-V_F))*V+n_min*V_D/(V_D-V_F)
    v_list.append(V)
    n_list.append(n)
while V_S1<V<V_F:
    V=V-1
    n=n_min
    v_list.append(V)
    n_list.append(n)
    
print(v_list, n_list)

    
    
    
    
