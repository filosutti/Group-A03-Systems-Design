#MINIMUM SPEED

def minSpeed(wps, V_appro,CLmax_Takeoff): 

    massfraction = 0.85
    density = 1.225

    minspeedtpw = (1/massfraction)*(density/2)*(V_appro/1.23)**2*(CLmax_Takeoff)

    return minspeedtpw