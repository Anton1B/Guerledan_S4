import numpy as np
import time
import arduino_driver_py3 as ard
from driver_capteur import *
from motor_py3 import *
from gps_driver_py3 import *


serial_arduino, data_arduino = ard.init_arduino_line()


maximum =   float(input("Maximum   : "))
temps   =   int(input("Temps     : "))
terme   =   float(input("Terme    : "))
#acc.choc=   int(input("Choc      : "))

commande = Commande(serial_arduino)

t0 = time.time()
capteur = Capteur(t0,True,temps*1.05)

#direction = (360-direction)*np.pi/180

"""
def orient(capteur):
	vect = capteur.get_Cap()
	X,Y=vect[0],vect[1]
	norme = (X**2+Y**2)**0.5
	X/=-norme
	Y/=norme
	angle = np.arccos(X)
	if Y<0:
		angle=2*np.pi-angle
	return angle
"""

mod = lambda x,y: x - (x//y)*y

def diffAngle(angle1,angle2):
	diff = angle1 - angle2 
	return mod(diff+np.pi,2*np.pi)-np.pi

def asservit(angle):
	angle-=terme*capteur.get_rot()
	D,G=1,1
	ouverture = 25*np.pi/180
	G = 0.5*(ouverture+angle)/ouverture
	D=1-G
	if abs(angle)>ouverture:
		if angle<0:
			G = 0
			D = 1
		else:
			G = 1
			D = 0
	return D**0.5,G**0.5

def get_angle(vect):
	vect = vect/np.linalg.norm(vect)
	angle = np.arccos(vect[1])
	if vect[0]>0:
		angle=2*np.pi-angle
	return angle

#triangle_pts = [np.array([48.199065000, -3.014733333]),np.array([48.198971, -3.014909]),np.array([48.198844, -3.014823])]
#triangle_pts = [np.array([48.198759000, -3.016019]),np.array([48.198971, -3.014909]),np.array([48.198844, -3.014823])]
triangle_pts = [np.array([48.199152000, -3.015528]),np.array([48.198971, -3.014909]),np.array([48.198844, -3.014823])]

for i in range(len(triangle_pts)):
	triangle_pts[i] = capteur.gps.transformeGPS_XY(triangle_pts[i])
#triangle_pts[0] = np.array([0.0,0.0])


capteur.start()
mode = 0
time.sleep(1)
dt = 0.25

for i in range(int(temps/dt)):
	if np.linalg.norm(triangle_pts[mode]-capteur.get_GPS())<=7.5:
		mode = (mode+1)%len(triangle_pts)
		print("CHANGE DE CIBLE")
	orientation = capteur.get_Cap()
	direction = get_angle(triangle_pts[mode]-capteur.get_GPS())
	
	angle = diffAngle(direction,orientation)
	
	print(capteur.gps.getVK())
	
	D,G = asservit(angle)
	commande.set(G*maximum,D*maximum)
	#ard.send_arduino_cmd_motor(serial_arduino,maximum*D,maximum*G)
	time.sleep(dt)
ard.send_arduino_cmd_motor(serial_arduino,0,0)

while not capteur.over:
	time.sleep(0.1)

