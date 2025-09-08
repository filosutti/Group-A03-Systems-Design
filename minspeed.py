#MINIMUM SPEED
#I think it's CLmax_Takeoff but might be CLmax_Landing

def minSpeed(wps, V_appro): 
    CLmax_Takeoff = 1.9
    density = 1.225
    massfraction = 0.85
    min = (1/massfraction)*(density/2)*(V_appro/1.23)**2*(CLmax_Takeoff)

    return min