#MINIMUM SPEED

def minSpeed(CLmax_Landing, massfraction, V_appro):
    density = 1.225 #kg/m^3 at sea level
    min = (1/massfraction)*(density/2)*((V_appro/1.23)**2)*(CLmax_Landing)

    return min