#MINIMUM SPEED

def minSpeed(wps, V_appro): 

    massfraction = 0.85
    CLmax_Takeoff = 1.9
    density = 1.225

    minspeedtpw = (1/massfraction)*(density/2)*(V_appro/1.23)**2*(CLmax_Takeoff)

    return minspeedtpw