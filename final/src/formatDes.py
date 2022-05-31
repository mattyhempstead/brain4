des = open("desig.txt", 'r')
out = ""
for line in des.readlines():
    out+=line.rstrip("\n")

print(out)