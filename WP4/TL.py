y_list = []
cl_list = []
cd_list = []
cm_list = []

import os
import sys

sys.path.append('..')


with open ('C:/Users/iorda/OneDrive/Desktop/GitHub/Group-A03-System-Design/WP4/XFLR_a_0.txt', 'r') as f:
    for line in f:
        if line.strip() == line.startswith("y-span") or len(line.split()) < 10 or float(line.split()[0]) < 0:
            continue
        
        parts = line.split()

        y = float(parts[0])
        cl = float(parts[3])
        cd = float(parts[5])   # total Cd? might want PCd+ICd depending on your use
        cm = float(parts[7])   # airfoil pitching moment at c/4

        y_list.append(y)
        cl_list.append(cl)
        cd_list.append(cd)
        cm_list.append(cm)

print(y_list)
print(cl_list)
print(cd_list)
print(cm_list)