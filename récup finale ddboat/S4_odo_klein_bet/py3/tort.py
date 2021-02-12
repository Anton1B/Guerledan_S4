import numpy as np
import time
import arduino_driver_py3 as ard
from driver_capteur import *
from motor_py3 import *
from gps_driver_py3 import *


serial_arduino, data_arduino = ard.init_arduino_line()


directionC = int(input("Direction : "))
maximum =   float(input("Maximum   : "))
temps   =   int(input("Temps     : "))
terme   =   float(input("Terme    : "))
#acc.choc=   int(input("Choc      : "))

commande = Commande(serial_arduino)

t0 = time.time()
capteur = Capteur(t0,True,temps+2)
gps = GPS(t0)

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

def diffAngle(angle1,angle2):
	diff = angle1 - angle2
	if diff>np.pi:
		diff-=2*np.pi
	if diff<-np.pi:
		diff+=2*np.pi
	return diff

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

cap_verrouille=False

capteur.start()
gps.start()
time.sleep(1)
directionC=int(360-capteur.get_Cap()*180/np.pi)
print(directionC)
direction=(360-directionC)*np.pi/180
for i in range(temps*20):
	orientation = capteur.get_Cap()
	angle = diffAngle(direction,orientation)
	if capteur.get_Choc():
		print("Choc")
		if abs(angle)<np.pi/6:
			directionC = (directionC+360-90)%360
			direction = (360-directionC)*np.pi/180
			cap_verrouille = False
			print("Chg Cap")
		commande.set(0,0)
		time.sleep(1)
	elif capteur.tropLong():
		commande.set(0,0)
		time.sleep(1)
	else:
		D,G = asservit(angle)
		commande.set(G*maximum,D*maximum)
		#ard.send_arduino_cmd_motor(serial_arduino,maximum*D,maximum*G)
		time.sleep(0.05)
ard.send_arduino_cmd_motor(serial_arduino,0,0)
gps.finit()
while not capteur.over:
	time.sleep(0.1)

