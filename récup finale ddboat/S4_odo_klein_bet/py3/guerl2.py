import numpy as np
import time
import arduino_driver_py3 as ard
from driver_capteur import *
from motor_py3 import *
from gps_driver_py3 import *


serial_arduino, data_arduino = ard.init_arduino_line()


maximum =   float(input("Maximum   : "))
temps   =   int(input("Temps     : "))
#terme   =   float(input("Terme    : "))
terme = 0.3
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

"""
for i in range(len(triangle_pts)):
	triangle_pts[i] = capteur.gps.transformeGPS_XY(triangle_pts[i])
"""
#triangle_pts[0] = np.array([0.0,0.0])


capteur.start()
mode = 0
time.sleep(1)
dt = 0.05

power = 0.0

A = triangle_pts[0]
A=capteur.gps.transformeGPS_XY(A)


B = triangle_pts[1]
B=capteur.gps.transformeGPS_XY(B)

A=np.array([-35,-40])
B=np.array([0,-5])

triangle_pts[0] = np.array([-5,0])
triangle_pts[1] = np.array([-65,0])
triangle_pts[2] = np.array([-35,-40])

def pos_obj(t):
	T = t-t0
	mode = int(3*T/temps)%3
	T = T-mode*(temps/3.)
	T = T/(temps/3.)
	#print("Temps : ",T)
	#print("Mode : ",mode)
	
	return (triangle_pts[(mode+1)%3]-triangle_pts[mode])*T + triangle_pts[mode]

def Lissajous(t):
	A = 40
	B = 20
	T = 200./2.
	x0 = -35
	y0 = 0
	a = (2*np.pi)/T
	b = np.pi/T
	t=t-t0
	return np.array([B*np.sin(a*t)+x0,A*np.sin(b*t+np.pi*0.)+y0])

"""
def pos_obj(t):
	T = t-t0
	return (B-A)*T/temps+A
"""



def gen_force(t, dt, f_pos_obj, pos_robot):
	v_obj = (f_pos_obj(t+dt) - f_pos_obj(t))/dt
	norm_v_obj = np.linalg.norm(v_obj)
	vec_boat_obj = f_pos_obj(t) - pos_robot
	return (norm_v_obj * vec_boat_obj)/5.0 + v_obj

def gen_forceL(t, Dt, f_pos_obj, pos_robot,w,dt):
	w2 = gen_force(t, Dt, f_pos_obj, pos_robot)
	Dw = w2-w
	w = w+Dw*dt
	return w

def control(w,capteur,power,dt):
	orientation = capteur.get_CapF()
	direction = get_angle(w)
	#print(direction*180/np.pi)
	angle = diffAngle(direction,orientation)
	
	#power += 10*(np.linalg.norm(w)-capteur.gps.getVK())*dt
	power = 0.63*np.linalg.norm(w)
	if power>1:
		power=1
	if power<0:
		power=0
	
	return angle,power

w=np.array([0,0])
while time.time()-t0<temps:
	#w=gen_forceL(time.time(), 1, pos_obj, capteur.gps.get(),w,dt)
	w=gen_force(time.time(), 1, Lissajous, capteur.gps.get())
	angle,power = control(w,capteur,power,dt)
	
	D,G = asservit(angle)
	commande.set(G*maximum*power,D*maximum*power)
	#ard.send_arduino_cmd_motor(serial_arduino,maximum*D,maximum*G)
	time.sleep(dt)
commande.set(0,0)
ard.send_arduino_cmd_motor(serial_arduino,0,0)

while not capteur.over:
	time.sleep(0.1)

