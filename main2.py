import threading
import time
from trajectory import trajectory
from Myboat import bateau
import numpy as np
def etat_bateau():
	while True :
		print(BATO.state())
		BATO.add_data_2_csv(traj.pt_cons)

	
BATO = bateau("nom")
traj = trajectory()
threading.Thread(target=etat_bateau).start()
Parcours = [np.array([[-30],[-50]]),np.array([[-50],[-30]]),np.array([[-20],[-20]])]
while True:
	traj.waypoint(BATO,Parcours,160)	
