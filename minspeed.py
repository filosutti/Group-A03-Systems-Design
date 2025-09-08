#MINIMUM SPEED
#I think it's CLmax_Takeoff but might be CLmax_Landing

def minSpeed(wps, V_appro): 
<<<<<<< HEAD
    CLmax_Takeoff = 1.9
    density = 1.225
    massfraction = 0.85
    min = (1/massfraction)*(density/2)*(V_appro/1.23)**2*(CLmax_Takeoff)
=======

    massfraction = 0.85
    CLmax_Takeoff = 1.9
    density = 1.225

    minspeedtpw = (1/massfraction)*(density/2)*(V_appro/1.23)**2*(CLmax_Takeoff)
>>>>>>> ecf72769a450fdd9f466273a720edd00d40c2f2a

    return minspeedtpw