des = open("desig.txt", 'r').read()
des_new = des.replace("1","0")

writer = open("desig.txt", 'w').write(des_new)