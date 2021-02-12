import serial
import os
import time
from threading import Thread
import numpy as np
from Kalman import Kalman

def init_line():
    ser = serial.Serial('/dev/ttyS0',timeout=1.0)
    time.sleep(1.0)
    print(ser)
    return ser

def read_gll(ser,nmax=20):
    val=[0.,'N',0.,'W',0.]
    for i in range(nmax):
        v=ser.readline().decode("utf-8")
        if str(v[0:6]) == "$GPGLL":
            break
    return v

def str_to_float(chaine):
	separe = chaine.split(".")
	value = float(separe[0][-4])*10+float(separe[0][-3])
	minute= float(separe[0][-2])*10+float(separe[0][-1])
	for i in range(4):
		minute+=float(separe[1][i])*0.1**(i+1)
	value += minute/60
	return value*np.pi/180.0   

def close(ser):
    ser.close()


class GPS(Thread):
	def __init__(self,t0,Kal = False,func=lambda:0):
		Thread.__init__(self)
		self.kalman = Kalman()
		self.gps = init_line()
		self.Kal = Kal
		self.t0 = t0
		self.over = False
		self.lastValue = np.array([0.0,0.0])
		self.lat0 = 48.199065000*np.pi/180.0
		self.lon0 = -3.014733333*np.pi/180.0
		self.R = 6371000
		self.func = func
	
	def finit(self):
		self.over = True
	
	def get(self):
		return self.lastValue;
	
	def transformeGPS_XY(self,vect):
		retour = np.array([0.0,0.0])
		retour[0] = self.R*np.cos(self.lat0)*(vect[1]*np.pi/180.0-self.lon0)
		retour[1] = self.R*(vect[0]*np.pi/180.0-self.lat0)
		return retour
	
	def getPK(self):
		return self.kalman.get_last()
	
	def getVK(self):
		return self.kalman.get_vit()
	
	def getSim(self):
		return self.kalman.get_sim()
	
	def run(self):
		fichier = open("gps_data.txt","w")
		while not self.over:
			value = str(time.time()-self.t0)+"#"+read_gll(self.gps);
			
			lol = value.split(",")
			try:
				lat = str_to_float(lol[1])
				lon = -str_to_float(lol[3])
				self.lastValue[0] = self.R*np.cos(self.lat0)*(lon-self.lon0)
				self.lastValue[1] = self.R*(lat-self.lat0)
				if self.Kal:
					self.kalman.integre1(self.func(),self.lastValue)
			except:
				print("Erreur GPS")
			fichier.write(str(self.kalman.get_vit())+"&"+str(self.func())+"&"+value)
		close(self.gps)

		fichier.close()
