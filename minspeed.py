#MINIMUM SPEED
#I think it's CLmax_Takeoff but might be CLmax_Landing

def minSpeed(CLmax_Takeoff, massfraction, V_appro):
    density = 1.225 #kg/m^3 at sea level
    min = (1/massfraction)*(density/2)*((V_appro/1.23)**2)*(CLmax_Takeoff)

    return min