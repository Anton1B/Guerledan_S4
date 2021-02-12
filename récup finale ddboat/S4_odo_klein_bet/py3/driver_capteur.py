import numpy as np
from cap_driver_py3 import *
from driver_acc import *
from threading import Thread
from gps_driver_py3 import *
import time

def transforme(diff):
	value=diff+7*np.pi
	return value-2*np.pi*int(value*0.5/np.pi)-np.pi

def pause(t,h,i):
	t+=h*(i+1)
	t2 = time.time()
	if t>t2:
		time.sleep(t-t2)
	else:
		#print("Prob t")
		a=1

def orient(vect):
	X,Y=vect[0],vect[1]
	norme = (X**2+Y**2)**0.5
	X/=-norme
	Y/=norme
	angle = np.arccos(X)
	if Y<0:
		angle=2*np.pi-angle
	return angle-np.pi


class Capteur(Thread):
	def __init__(self,t0,enrg=False,taille=1):
		Thread.__init__(self)
		self.gps = GPS(t0,True,self.get_Cap)
		self.over = False
		self.enrg = enrg
		self.taille = int(taille*100)
		self.t0=t0
		self.pos=-1
		self.cap = Cap_driver()
		self.acc = acc_driver()
		self.sensibilite = 250
		self.listeChoc=[0]
		self.impact = False
		self.data = []
		for i in range(self.taille):
			self.data.append([i*0.01,np.array([0,0,0]),0,np.array([0,0,0,0,0,0]),0])
		self.data[-1][2]=orient(self.cap.get())
		self.data[-1][4]=orient(self.cap.get())
		self.offset=0
		self.offset2=0
		self.moyenneFait = False
		
	
	def finit(self):
		self.over = True
	
	def sauve(self):
		fichier = np.zeros((self.taille,12))
		for i in range(self.taille):
			fichier[i,0]=self.data[i][0]
			fichier[i,1:4]=self.data[i][1][:]
			fichier[i,4:10]=self.data[i][3][:]
			fichier[i,11]=self.data[i][2]
			fichier[i,10]=self.data[i][4]
		np.savetxt("all_data.txt",fichier)
		np.savetxt("impact_time.txt",np.array(self.listeChoc))
	
	def filtre(self,Id):
		nouv = orient(self.data[Id][1])
		self.data[Id][4]=nouv
		rot = (4*360./165.69)*0.01*(self.data[Id][3][5]-self.offset)*np.pi/(180.*1000.)
		diff1 = transforme(nouv-self.data[self.pos][2])
		diff2 = rot
		if self.moyenneFait:
			return transforme(self.data[self.pos][2]+(0.995*diff2+0.005*diff1))
		else:
			return transforme(self.data[self.pos][2]+diff1)
	
	def run(self):
		i=0
		h=0.01
		self.gps.start()
		tstart = time.time()
		while not self.over and (i<self.taille or not self.enrg):
			Id = i%self.taille
			self.data[Id][0] = time.time()-self.t0
			self.data[Id][1] = self.cap.get()
			self.data[Id][3] = self.acc.get()
			if self.moyenneFait and self.data[Id][3][0]-self.offset2>self.sensibilite and self.listeChoc[-1]+2<time.time()-self.t0:
				self.listeChoc.append(time.time()-self.t0)
				self.impact = True
			self.data[Id][2]=self.filtre(Id)
			self.pos=Id
			if i==99:
				self.offset=0
				for k in range(100):
					#self.offset+=0.01*self.data[k][3][5]
					self.offset2+=0.01*self.data[k][3][0]
				self.offset = 4742.5
				self.moyenneFait=True
			pause(tstart,h,i)
			i+=1
		if self.enrg:
			self.sauve()
		self.gps.finit()
		self.over = True
	
	def get_CapF(self):
		return self.data[self.pos][2]+np.pi
	
	def get_Cap(self):
		return transforme(orient(self.data[self.pos][1]))+np.pi
	
	def get_GPS(self):
		return self.gps.get()
	
	def get_rot(self):
		return transforme(self.data[self.pos][2]-self.data[(self.pos-5+self.taille)%self.taille][2])/0.05
	
	def get_Choc(self):
		if self.impact:
			self.impact = False
			return True
		return False
	
	def tropLong(self):
		if (time.time()-self.t0-self.listeChoc[-1])>20:
			self.listeChoc.append(time.time()-self.t0)
			return True
		return False







