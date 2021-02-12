import threading
import time
from trajectory import trajectory
from Myboat import bateau
import numpy as np
def etat_bateau():
	while True :
		BATO.state()
		BATO.add_data_2_csv(traj.pt_cons)
		#BATO.add_data_2_csv(np.array([[-30],[-30]]))

nom = str(input("Mission name"))	
BATO = bateau("nom")

traj = trajectory()
threading.Thread(target=etat_bateau).start()
Parcours = [np.array([[-30],[-30]]),np.array([[-50],[-30]]),np.array([[-20],[-20]])]
choix = int(input("Triagle {1}, point {2}"))
while True:
	if choix == 1 :
		traj.waypoint(BATO,Parcours,1)
	elif choix == 2 :
		traj.unpoint(BATO,Parcours[1])

