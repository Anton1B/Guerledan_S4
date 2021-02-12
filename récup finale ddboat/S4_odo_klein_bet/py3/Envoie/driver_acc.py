import time
import smbus
import numpy as np
from threading import Thread



# Calculate the 2's complement of a number
def twos_comp(val1, val2):
	a1 = np.int16(val1)
	a2 = np.int16(val2)
	return np.int16((a2<<8)+a1)

def byteToNumber(val_1,val_2):
        number = 256 * val_2 + val_1
        if number >= 32768:
                number= number - 65536
        return number



"""def read_boussole():
	val = bus.read_i2c_block_data(i2c_address, 0x28, 6)
	return val"""
	

#print(read_boussole())
	
class acc_driver(Thread):
	def __init__(self):
		self.choc=500
		self.impact = False
		i2c_ch = 1
		Thread.__init__(self)
		self.over = False
		# TMP102 address on the I2C bus
		self.i2c_address = 0x6b
		

		# Register addresses
		reg_temp = 0x00
		reg_config = 0x01
		self.reg = 0x28
		self.bus = smbus.SMBus(i2c_ch)
		#       1    2
		Ctrl = [0x57,0x50]
		self.bus.write_i2c_block_data(self.i2c_address,0x10,Ctrl)
		#       5    6    7    8    9    10
		Ctrl = [0x64,0x20,0x00,0xa5,0x38,0x3d]
		self.bus.write_i2c_block_data(self.i2c_address,0x14,Ctrl)
		"""
		#CTRL1_XL
		self.bus.write_byte_data(self.i2c_address,0x10,0b10100111)

		#CTRL2_G
		self.bus.write_byte_data(self.i2c_address,0x11,0x40)

		#CTRL5_C
		self.bus.write_byte_data(self.i2c_address,0x14,0b01100100)

		#CTRL6_C
		self.bus.write_byte_data(self.i2c_address,0x15,0b00100000)

		#CTRL7_G
		self.bus.write_byte_data(self.i2c_address,0x16,0x44)
		"""
	
	def finit(self):
		self.over = True
	
	def tourne(self):
		if self.impact!=0:
			lol = self.impact
			self.impact = 0
			return lol
		return 0
	
	def run(self):
		dt = 0.01
		t1 = time.time()
		liste = []
		filtre = 0
		memo = 0
		derive = 0
		while not self.over:
			vect = self.get()
			memo = filtre
			filtre = filtre*0.8 + vect[5]*0.2
			derive = filtre - memo
			if abs(derive) > self.choc and time.time()-t1>1.5:
				self.impact = np.sign(derive)
				t1 = time.time()
				print("CHOC !!! ",derive)
			liste.append(vect)
			time.sleep(dt)
		np.savetxt("data_acc.txt",np.array(liste))

	def get(self):
		#Read acc x   0x28 & 0x29  

		AX = byteToNumber(self.bus.read_byte_data(self.i2c_address, 0x28),self.bus.read_byte_data(self.i2c_address, 0x29))

		#Read acc y   0x2a & 0x2b
		AY = byteToNumber(self.bus.read_byte_data(self.i2c_address, 0x2A),self.bus.read_byte_data(self.i2c_address, 0x2B))

		#Read acc z   0x2c & 0x2d
		AZ = byteToNumber(self.bus.read_byte_data(self.i2c_address, 0x2C),self.bus.read_byte_data(self.i2c_address, 0x2D))

		#Read gyro x   0x22 & 0x23  
		GX = byteToNumber(self.bus.read_byte_data(self.i2c_address, 0x22),self.bus.read_byte_data(self.i2c_address, 0x23))

		#Read gyro y   0x24 & 0x25
		GY = byteToNumber(self.bus.read_byte_data(self.i2c_address, 0x24),self.bus.read_byte_data(self.i2c_address, 0x25))

		#Read gyro z   0x26 & 0x27
		GZ = byteToNumber(self.bus.read_byte_data(self.i2c_address, 0x26),self.bus.read_byte_data(self.i2c_address, 0x27))
		return np.array([AX, AY, AZ, GX, GY, GZ])



