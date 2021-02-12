import time
import smbus
import numpy as np

def complementA2(val1,val2):
	a1 = np.int16(val1)
	a2 = np.int16(val2)
	return np.int16((a2<<8) + a1)


class Cap_driver:
	def __init__(self):
		i2c_ch = 1
		self.i2c_address = 0x1e
		self.reg = 0x28
		self.bus = smbus.SMBus(i2c_ch)#[]
		self.bus.write_i2c_block_data(0x1e,0x20,[0xbc,0x00,0x00,0x04,0x40])
		self.M=np.loadtxt("calibre_cap.txt")
	
	def get(self):
		val = self.bus.read_i2c_block_data(self.i2c_address, self.reg,6)
		compl = np.array([complementA2(val[0],val[1]),complementA2(val[2],val[3]),complementA2(val[4],val[5])])
		return (compl+self.M[0])*self.M[1]
	
	def getBrut(self):
		val = self.bus.read_i2c_block_data(self.i2c_address, self.reg,6)
		compl = np.array([complementA2(val[0],val[1]),complementA2(val[2],val[3]),complementA2(val[4],val[5])])
		return compl