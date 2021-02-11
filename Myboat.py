import smbus
import numpy as np
from numpy import cos,sin,arctan2,pi,array
import arduino_driver_py3 as ard
import gps_driver_py3 as gpsdrv
import csv
import socket
import time

DEVICE_ADDRESS = 0x1e      
CTRL_REG1=0x20
CTRL_REG2=0x21
CTRL_REG3=0x22
CTRL_REG4=0x23
CTRL_REG5=0x24

ACCEL_ADRESS = 0X6b
#fifo_ctrl
FIFO_CTRL1 = 0x06
FIFO_CTRL2 = 0x07
FIFO_CTRL3 = 0x08
FIFO_CTRL4 = 0x09
FIFO_CTRL5 = 0x0A

WHO_AM_I = 0x0F
#CTRL
CTRL1_XL = 0x10
CTRL2_G = 0x11
CTRL3_C = 0x12
CTRL4_C = 0x13
CTRL5_C = 0x14
CTRL6_C = 0x15
CTRL7_G = 0x16
CTRL8_XL = 0x17
CTRL9_XL = 0x18
CTRL10_C = 0x19

#adresseaccel
OUTX_L_XL = 0x28
OUTX_H_XL = 0x29
OUTY_L_XL = 0x2A
OUTY_H_XL = 0x2B
OUTZ_L_XL = 0x2C
OUTZ_H_XL = 0x2D

OUT_X_L = 0b00101000
OUT_Y_L = 0b00101010
OUT_Z_L = 0b00101100

LAT0 = (48.19906500)*2*pi/360
LONG0 = (-3.01473333)*2*pi/360
RAYON_TERRE = 6371000 #m

class bateau():

	def __init__(self,mission_name):
		self.mission_name = mission_name
		self.vmax = 120
		self.vmin = 0
		self.x = 0
		self.y = 0
		self.Kregulcap = 0.2
		self.u1 = 0
		self.u2 = 0
		self.lat = 0
		self.long = 0
		self.gps_time = 0
		self.bus = smbus.SMBus(1)
		self.gps = gpsdrv.init_line()
		self.p0 = np.array([[3383],[-2221],[4617],[1/3070],[1/3070],[1/3070],[0],[0],[0]])
		self.arduino = ard.init_arduino_line()[0]
		#basicoffset
		self.bus.write_byte_data(ACCEL_ADRESS,FIFO_CTRL1, 0b00000000)
		self.bus.write_byte_data(ACCEL_ADRESS,FIFO_CTRL2, 0b00000000)
		self.bus.write_byte_data(ACCEL_ADRESS,FIFO_CTRL3, 0b00000000)
		self.bus.write_byte_data(ACCEL_ADRESS,FIFO_CTRL4, 0b00000000)
		self.bus.write_byte_data(ACCEL_ADRESS,FIFO_CTRL5, 0b00000000)
		#capteurregl
		self.bus.write_byte_data(ACCEL_ADRESS,CTRL1_XL, 0b01010111)
		self.bus.write_byte_data(ACCEL_ADRESS,CTRL2_G, 0b01010000)
		self.bus.write_byte_data(ACCEL_ADRESS,CTRL3_C, 0b00000100)
		self.bus.write_byte_data(ACCEL_ADRESS,CTRL4_C, 0b00000000)
		self.bus.write_byte_data(ACCEL_ADRESS,CTRL5_C, 0b01100100)
		self.bus.write_byte_data(ACCEL_ADRESS,CTRL6_C, 0b00100000)
		self.bus.write_byte_data(ACCEL_ADRESS,CTRL7_G, 0b00000000)
		self.bus.write_byte_data(ACCEL_ADRESS,CTRL8_XL, 0b10100101)
		self.bus.write_byte_data(ACCEL_ADRESS,CTRL9_XL, 0b00111000)
		self.bus.write_byte_data(ACCEL_ADRESS,CTRL10_C, 0b00111101)
		# open socket comunication
		# Attempt connexion to server.
		try:
			self.HOST = ('172.20.26.195') # Mettre ton addresse IP (ifconfig)
			self.PORT = 50000
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.client.connect((self.HOST, self.PORT))
			print ('Connexion vers ' + self.HOST + ':' + str(self.PORT) + ' reussie.')
		except ConnectionRefusedError:
			print ("Connexion impossible")

	def position(self):
	    val = gpsdrv.read_gll(self.gps)
	    self.gps_time = val[4]
	    self.lat = val[0]
	    self.long = val[2]
	    lat = val[0]*2*pi/360
	    longi = val[2]*2*pi/360	
	    self.x = RAYON_TERRE*np.cos(lat)*(longi-LONG0)
	    self.y = RAYON_TERRE*(lat-LAT0)

	def cap(self):
	  self.bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_REG4, [0b00000000])
	  self.bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_REG3, [0b00000000])
	  ledout_values_x = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
	  ledout_values_y = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
	  ledout_values_z = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
	  ledout_values_x = self.bus.read_i2c_block_data(DEVICE_ADDRESS, OUT_X_L,2)
	  x = ledout_values_x[0] + ledout_values_x[1]*256
	  if x > 32767 : # 2p15 -1
	      x = x - 65536 # 2p16
	  ledout_values_y = self.bus.read_i2c_block_data(DEVICE_ADDRESS, OUT_Y_L,2)
	  y = ledout_values_y[0] + ledout_values_y[1] * 256
	  if y > 32767:
	      y = y - 65536
	  ledout_values_z = self.bus.read_i2c_block_data(DEVICE_ADDRESS, OUT_Z_L,2)
	  z = ledout_values_z[0] + ledout_values_z[1] * 256
	  if z > 32767:
	      z = z - 65536
	  N = np.array([[x], [y], [z]])
	  N2 = fp(N,self.p0)
	  x2 = N2[0,0]
	  y2 = N2[1, 0]
	  z2 = N2[2, 0]
	  cap_m2 = np.arctan2(y2, x2)
	  cap_m2 = cap_m2 * (180 / np.pi)
	  if cap_m2<0 :
	    cap_m2+=360
	  return cap_m2*2*pi/360
	  
	def state(self):
		self.position()
		return array([[self.x],[self.y],[self.cap()]])

	def set_speed(self,u1,u2):
		self.u1 = max(min(u1,self.vmax),self.vmin)
		self.u2 = max(min(u2,self.vmax),self.vmin)
		ard.send_arduino_cmd_motor(self.arduino, self.u1, self.u2)
		return True

	def regul_cap(self,capd):
		#capd est le cap consigne
		e = sawtooth((self.cap() - capd)*2*np.pi/360)
		#v = ((abs(e)*(self.vmax - self.vmin)) / np.pi) + self.vmin
		u1 = max(min(int(40*(1 + self.Kregulcap *e)),self.vmax),0)
		u2 = max(min(int(40*(1 - self.Kregulcap *e)),self.vmax),0)
		self.set_speed(u2,u1)
		
	def safety_turn(self):
		self.set_speed(50,0)
	
	def safety_return(self):
		self.set_speed(50,50)
	
	def send_msg(self,message):
		time.sleep(0.1)
		# message = (b'Hello, world')
		# print (b'Envoi de :' + message)
		n = self.client.send(message)
		if (n != len(message)):
				print ('Erreur envoi.')
		else:
				print ('Envoi ok.')
		# print ('Reception...')
		# donnees = client.recv(1024)
		# print ('Recu :', donnees)
		# print ('Deconnexion.')
		# client.close()

	def add_data_2_csv(self, target):
		""" 
		Write class data to CSV file
		Entries :
		csv_name: name of the file to write
		x: DD pos
		y: DD pos
		h: hour
		u1: fan 
		u2: fan
		cap : X[2]
		target: array 2D x,y a convertir en DD
		"""
		# Opening mission data log.
		with open("./gps_data_logs/"+self.mission_name + ".csv","a") as self.csv_file:
			fieldnames=['lat','long','h','u1','u2','cap','target_x','target_y']
			csv_writer=csv.DictWriter(self.csv_file, fieldnames=fieldnames)
			# csv_writer = writer(self.csv_file)
			csv_writer.writerow({	'lat': self.lat,
								'long': self.long,
								'h': self.gps_time,
								'u1': self.u1,
								'u2': self.u2,
								'cap': self.cap(),
								'target_x': target[0],
								'target_y': target[1]})
			self.csv_file.flush()

		# a tester. envoie message au serveur.
		test = (self.lat,self.long,self.gps_time,self.u1,self.u2,self.cap(),target[0][0],target[1][0])
		try:
			pass
			self.send_msg(str(test).encode('utf-8'))
		except BrokenPipeError:
			pass

def sawtooth(x):
    return (x+2*np.pi)%(2*np.pi)-np.pi
 
def fp(x,p0):
    I1 = np.array([[p0[3,0],p0[6,0],p0[8,0]],
              [p0[6,0],p0[4,0],p0[7,0]],
              [p0[8,0],p0[7,0],p0[5,0]]])
    I2 = np.array([[p0[0,0]],[p0[1,0]],[p0[2,0]]])
    return I1 @ (x-I2)

	
