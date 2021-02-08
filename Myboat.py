import smbus
import numpy as np
import arduino_driver_py3 as ard

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

class bateau():
	def __init__(self):
		self.vmax = 80
		self.vmin = 15
		self.Kregulcap = 1
		self.bus = smbus.SMBus(1)
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
	  return cap_m2

	def set_speed(self,u1,u2):
		ard.send_arduino_cmd_motor(self.arduino, u1, u2)
		return True

	def regul_cap(self,capd):
		#capd est le cap consigne
		e = sawtooth((self.cap() - capd)*2*np.pi/360)
		#v = ((abs(e)*(self.vmax - self.vmin)) / np.pi) + self.vmin
		print(e)
		u1 = min(int(0.5*80*(1 + self.Kregulcap *e)),self.vmax)
		u2 = min(int(0.5*80*(1 - self.Kregulcap *e)),self.vmax)
		self.set_speed(u1,u2)
def sawtooth(x):
    return (x+2*np.pi)%(2*np.pi)-np.pi
	 
def fp(x,p0):
    I1 = np.array([[p0[3,0],p0[6,0],p0[8,0]],
              [p0[6,0],p0[4,0],p0[7,0]],
              [p0[8,0],p0[7,0],p0[5,0]]])
    I2 = np.array([[p0[0,0]],[p0[1,0]],[p0[2,0]]])
    return I1 @ (x-I2)
