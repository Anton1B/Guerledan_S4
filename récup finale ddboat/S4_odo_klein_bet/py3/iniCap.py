from cap_driver_py3 import *
import numpy as np
import time

cap = Cap_driver()
lol = []
print("Commence...\n")
for i in range(6000):
	lol.append(cap.getBrut())
	time.sleep(0.01)
	

lol=np.array(lol)

M = np.zeros((2,3))
for i in range(3):
	M[0,i] = -(max(lol.T[i])+min(lol.T[i]))/2
	M[1,i] =  1/((max(lol.T[i])-min(lol.T[i]))/2)

print(M)
np.savetxt("calibre_cap.txt",M)