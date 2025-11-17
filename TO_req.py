import numpy as np
def TOF_req(WpS):
    TOreq = 1296
    Cd0 = 0.0162
    e = 0.8045
    CLmax_Takeoff = 1.9
    g = 9.81
    AR = 9
    Speed_ratio = 1.13
    Cl2 = Speed_ratio**2 * CLmax_Takeoff
    kt = 0.85
    ptr = 1.4802
    Ttr = 1.1186
    BPR = 12
    #flap adjustment
    Cd0_TO = Cd0 + 0.0013*15 + 0.015
    e_TO = e + 0.0026*15

    #alpha_t
    alpha_t = ptr*(1-(0.43 + 0.014*BPR)*np.sqrt(0.77) - 3*(Ttr - 1.07)/(2.27))
    #take off field length
    Tpw6 = (1/alpha_t)*(1.15)*(np.sqrt((WpS)/(kt*1.225*TOreq*g*np.pi*AR*e_TO))+ 4*10.7/TOreq)
    return Tpw6