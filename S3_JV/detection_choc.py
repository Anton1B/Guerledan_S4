#!/usr/bin/python
import time
import smbus
import numpy as np
import arduino_driver_py3 as ardudrv


bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

DEVICE_ADDRESS = 0x6b     #7 bit address (will be left shifted to add the read write bit)

CTRL_1_XL=0x10
CTRL_2_XL=0x11
CTRL_5_XL=0x14
CTRL_6_XL=0x15
CTRL_7_XL=0x16
CTRL_8_XL=0x17
CTRL_9_XL=0x18
CTRL_10_XL=0x19







OUTX_L_G = 0x28
OUTY_L_G = 0x2A
OUTZ_L_G = 0x2C

bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_1_XL, [0b01010111])
bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_2_XL, [0b01010000])
bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_5_XL, [0b01100100])
bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_6_XL, [0b00100000])
bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_7_XL, [0b00000000])
bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_8_XL, [0b10100101])
bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_9_XL, [0b00111000])
bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_10_XL, [0b00111101])



ledout_values_x = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
ledout_values_y = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
ledout_values_z = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]


tmax = 100

import csv

# INITIALISATION MOTEURS
duration = 30.0
serial_arduino, data_arduino = ardudrv.init_arduino_line()
timeout = 1.0
data_arduino = ardudrv.get_arduino_status(serial_arduino,timeout)
t0 = time.time()

cmdl = 130
cmdr = 100
u = np.array([[cmdr],[cmdl]])

t=0

def av(X) :
    somme = 0
    for i in X :
        somme+=i
    return somme/len(X)





C = []


test = 0
nb_chocs = 0

flag = 0
t1=2601602769
interc = 1.0
# FONCTIONNEMENT DES MOTEURS
while (time.time()-t0) < duration:
    t=(time.time()-t0)
    ardudrv.send_arduino_cmd_motor(serial_arduino,u[0,0],u[1,0])

    ledout_values_x = bus.read_i2c_block_data(DEVICE_ADDRESS, OUTX_L_G,2)
    x = ledout_values_x[0] + ledout_values_x[1]*256
    if x > 32767 : # 2p15 -1
        x = x - 65536 # 2p16


    ledout_values_y = bus.read_i2c_block_data(DEVICE_ADDRESS, OUTY_L_G,2)
    y = ledout_values_y[0] + ledout_values_y[1] * 256
    if y > 32767:
        y = y - 65536


    ledout_values_z = bus.read_i2c_block_data(DEVICE_ADDRESS, OUTZ_L_G,2)
    z = ledout_values_z[0] + ledout_values_z[1] * 256
    if z > 32767:
        z = z - 65536



    x-=173
    y+=212
    mx = np.abs(x)
    my = np.abs(y)
    C.append(mx+my)


    if len(C)>10:
        test = av(C)
        C.pop(0)
    
    #print(test)

    if test > 460 and flag==0:
        t1 = time.time()
        cmdl = 0
        cmdr = 0
        u = np.array([[cmdr],[cmdl]])
        flag = 1
    
    print(test)
    if time.time()-t1 >1.0:
        nb_chocs+=1
        t1 = 2601602769
        flag = 0
        print("CHOC")
        cmdl = 130
        cmdr = 100
        u = np.array([[cmdr],[cmdl]])
    time.sleep(0.1)




# ARRETS MOTEURS
cmdl = 0
cmdr = 0
ardudrv.send_arduino_cmd_motor(serial_arduino,cmdl,cmdr)

print(nb_chocs)