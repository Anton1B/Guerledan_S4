from Myboat import bateau,sawtooth
import time
import trajectory as traj
import numpy as np
from numpy import array
print("Programm Starting")

t0 = time.time()
nom=str(input("Indiquer le nom de la mission"))
Myboat = bateau(nom)

Myboat.set_speed(0,0)
time.sleep(4)
Parcours = [np.array([[-30],[-50]]),np.array([[-50],[-30]])]#,np.array([[-20],[-20]])]
traj.triangle(Myboat)
#traj.waypoint(Myboat,Parcours,160)
#traj.unpoint(Myboat,array([[-30],[-30]]))
#traj.unpoint_v2(Myboat,array([[-30],[-30]]))
#traj.waypoint2(Myboat, Parcours,1)
"""
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
print("MISSION DURATION", time.time()-t0)"""


