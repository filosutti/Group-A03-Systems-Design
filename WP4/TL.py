ylst = []
cllst = []
cdlst = []
cmlst = []

# hello

with open ('WP4/XFLR0.txt','r') as f:
    for line in f:
        parts = line.split()

        y = float(parts[0])
        cl = float(parts[3])
        cd = float(parts[5])   
        cm = float(parts[7])   

        ylst.append(y)
        cllst.append(cl)
        cdlst.append(cd)
        cmlst.append(cm)

print("ylst", ylst)
print("clst", cllst)
print("cdlst", cdlst)
print("cmlst", cmlst)






















