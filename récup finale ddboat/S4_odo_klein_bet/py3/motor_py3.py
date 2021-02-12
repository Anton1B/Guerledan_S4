import numpy as np
from threading import Thread
import time
import encoders_driver_py3 as encodrv
import arduino_driver_py3 as ard
import sys
import encoders_driver_py3 as encodrv

def delta_odo (odo1,odo0):
    dodo = odo1-odo0
    if dodo > 32767:
        dodo -= 65536
    if dodo < -32767:
        dodo += 65536
    return dodo

class Commande(Thread):
	def __init__(self,serial,init=False,pas=25,adresse="parametre_moteur.txt"):
		self.serial=serial
		self.adresse=adresse
		self.pas = pas
		self.moteurG = np.array([[],[]])
		self.moteurD = np.array([[],[]])
		if init:
			self.init()
		else:
			self.charge()
			self.maximum = min(self.moteurG[1,10],self.moteurD[1,10])
	
	def fonc(self,M,val):
		val*=self.maximum
		if val<=M[1,0]:
			return M[0,0]
		if val>=M[1,10]:
			return M[0,10]
		for i in range(1,11):
			if val<M[1,i]:
				return (M[0,i]-M[0,i-1])*(val-M[1,i-1])/(M[1,i]-M[1,i-1])+M[0,i-1]
		return 0
			
	
	def set(self,G,D):
		ard.send_arduino_cmd_motor(self.serial,self.fonc(self.moteurD,D),self.fonc(self.moteurG,G))
	
	def charge(self):
		A = np.loadtxt(self.adresse)
		self.moteurG = A[0:2,:]
		self.moteurD = A[2:4,:]
	
	def init(self):
		A=np.zeros((4,11))
		encodrv.set_baudrate(baudrate=115200)
		for i in range(11):
			consigne = i*self.pas
			A[0,i]=consigne
			A[2,i]=consigne
			ard.send_arduino_cmd_motor(self.serial,consigne,consigne)
			time.sleep(0.5)
			sync0, timeAcq0, sensLeft0, sensRight0, posLeft0, posRight0 =  encodrv.read_single_packet(debug=True)
			time.sleep(1)
			sync0, timeAcq0, sensLeft0, sensRight0, posLeft1, posRight1 =  encodrv.read_single_packet(debug=True)
			A[1,i]=abs(delta_odo(posLeft1,posLeft0))
			A[3,i]=abs(delta_odo(posRight1,posRight0))
		ard.send_arduino_cmd_motor(self.serial,0,0)
		np.savetxt(self.adresse,A)


			