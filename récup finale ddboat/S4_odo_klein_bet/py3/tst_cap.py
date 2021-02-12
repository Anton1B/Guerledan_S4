import numpy as np
from cap_driver_py3 import Cap_driver
import time
import arduino_driver_py3 as ard
from driver_acc import *

cap = Cap_driver()
serial_arduino, data_arduino = ard.init_arduino_line()
acc = acc_driver()


directionC = int(input("Direction : "))
maximum =   int(input("Maximum   : "))
temps   =   int(input("Temps     : "))
#acc.choc=   int(input("Choc      : "))

#direction = (360-direction)*np.pi/180

def orient(cap):
	vect = cap.get()
	X,Y=vect[0],vect[1]
	norme = (X**2+Y**2)**0.5
	X/=-norme
	Y/=norme
	angle = np.arccos(X)
	if Y<0:
		angle=2*np.pi-angle
	return angle

def diffAngle(angle1,angle2):
	diff = angle1 - angle2
	if diff>np.pi:
		diff-=2*np.pi
	if diff<-np.pi:
		diff+=2*np.pi
	return diff

def asservit(angle):
	D,G=1,1
	ouverture = 10*np.pi/180
	if angle<0:
		G = (ouverture/2+angle/2)/ouverture+0.5
	else:
		D = (ouverture/2+angle/2)/ouverture+0.5
	if abs(angle)>ouverture:
		if angle<0:
			G = 0
			D = 1
		else:
			G = 1
			D = 0
	return D,G

acc.start()
for i in range(temps*10):
	directionC = (directionC+360-90*acc.tourne())%360
	direction = (360-directionC)*np.pi/180
	orientation = orient(cap)
	angle = diffAngle(direction,orientation)
	D,G = asservit(angle)
	ard.send_arduino_cmd_motor(serial_arduino,maximum*D,maximum*G)
	time.sleep(0.1)
acc.finit()
ard.send_arduino_cmd_motor(serial_arduino,0,0)

