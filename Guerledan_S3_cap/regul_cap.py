#!/usr/bin/python
import time
import smbus
import numpy as np


bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

DEVICE_ADDRESS = 0x1e      #7 bit address (will be left shifted to add the read write bit)

CTRL_REG1=0x20
CTRL_REG2=0x21
CTRL_REG3=0x22
CTRL_REG4=0x23
CTRL_REG5=0x24

OUT_X_L = 0b00101000
OUT_Y_L = 0b00101010
OUT_Z_L = 0b00101100

bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_REG4, [0b00000000])

bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_REG3, [0b00000000])


ledout_values_x = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
ledout_values_y = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
ledout_values_z = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]


tmax = 1000

p0 = np.array([[1886],[-3507],[6048.5],[1/3000],[1/3000],[1/3000],[0],[0],[0]]) # forme une matrice identité

def fp(x,p0):
    I1 = np.array([[p0[3,0],p0[6,0],p0[8,0]],
              [p0[6,0],p0[4,0],p0[7,0]],
              [p0[8,0],p0[7,0],p0[5,0]]])
    I2 = np.array([[p0[0,0]],[p0[1,0]],[p0[2,0]]])
    return I1 @ (x-I2)



for i in range (tmax) :
    ledout_values_x = bus.read_i2c_block_data(DEVICE_ADDRESS, OUT_X_L,2)
    x = ledout_values_x[0] + ledout_values_x[1]*256

    if x > 32767 : # 2p15 -1
        x = x - 65536 # 2p16


    ledout_values_y = bus.read_i2c_block_data(DEVICE_ADDRESS, OUT_Y_L,2)
    y = ledout_values_y[0] + ledout_values_y[1] * 256

    if y > 32767:
        y = y - 65536

    ledout_values_z = bus.read_i2c_block_data(DEVICE_ADDRESS, OUT_Z_L,2)
    z = ledout_values_z[0] + ledout_values_z[1] * 256

    if z > 32767:
        z = z - 65536
    #print(x,y,z)

    N = np.array([[x], [y], [z]])
    N2 = fp(N,p0)

    x2 = N2[0,0]
    y2 = N2[1, 0]
    z2 = N2[2, 0]

    #print(x2, y2, z2)

    cap_m = abs(np.arctan2(y,x))

    cap_m2 = np.arctan2(y2, x2)

    cap_m = cap_m*(180/np.pi)



    cap_m2 = cap_m2 * (180 / np.pi)
    if cap_m2<0 :
        cap_m2+=360
    print(cap_m2)
    print()
    time.sleep(0.1)

