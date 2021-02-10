from Myboat import bateau,sawtooth
import time
import trajectory as traj
import numpy as np
from numpy import array
print("Programm Starting")

t0 = time.time()
nom=str(input("Indiquer le nom de la mission"))
Myboat = bateau(nom)
Parcours = [np.array([[-8],[-42]]),np.array([[-30],[-30]]),np.array([[-18],[-70]])]
#traj.triangle(Myboat)
#traj.waypoint(Myboat,Parcours,160) 


i = 0
X = []
Y = []
while i<100:
	t1 = time.time()
	i +=1
	Myboat.position()
	print(Myboat.x)
	print(Myboat.y)	
	X.append(Myboat.x)
	Y.append(Myboat.y)
X.sort()
Y.sort()
print("X moyen =", X[49])
print("Y moyen =", Y[49])
Myboat.set_speed(0,0)
print("MISSION DURATION", time.time()-t0)


