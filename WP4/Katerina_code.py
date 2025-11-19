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

a_cruise = ISA(h_cruise)[3]
V_c = a_cruise * M_cr

# it is defined the speed above which structural integrity is not guaranteed if the control surfaces are fully deflected.
#  𝑛 is the limit positive manoeuvring load factor at 𝑉_𝐶
def Veq(CL, m, h):
    T, P, Rho, a=ISA(h)
    v=((2*9.80665*m)/(Rho*CL*62.8299727939332))**0.5
    return(v)

def nvdiagram(h, m, n_max):
    V_S0ap=Veq(CL_maxap, m, h)
    V_S0to=Veq(CL_maxto, m, h)
    V_S1=Veq(CL_maxcr, m, h)
    V_a = V_S1*(n_max)**0.5 
    V_d = V_c * 1.25
    V_F1 = V_S1 * 1.6 # with the wing-flaps in take-off position at maximum take-off weight
    V_F2 = V_S1 * 1.8 #with the wing-flaps in approach position at maximum landing weight
    V_F3 = V_S0ap * 1.8 # with the wing-flaps in landing position at maximum landing weight
    V_F = max(V_F1, V_F2, V_F3)
    return (V_S0ap, V_S0to, V_S1, V_a, V_d, V_F1, V_F2, V_F3, V_F)


#def V_F(V_S1, V_S0): # V_S1 and V_S0 should already be in equivalent airspeed
   # V_F1 = V_S1 * 1.6 # with the wing-flaps in take-off position at maximum take-off weight
   # V_F2 = V_S1 * 1.8 #with the wing-flaps in approach position at maximum landing weight
   # V_F3 = V_S0 * 1.8 # with the wing-flaps in landing position at maximum landing weight
  #  V_F = max(V_F1, V_F2, V_F3)
  #  return(V_F)
