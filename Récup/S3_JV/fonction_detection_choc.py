#!/usr/bin/python
import time
import smbus
import numpy as np
import arduino_driver_py3 as ardudrv

#Fonction moyenne
def av(X) :
    somme = 0
    for i in X :
        somme+=i
    return somme/len(X)




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

def get_choc():
    # Ecriture registres
    bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_1_XL, [0b01010111])
    bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_2_XL, [0b01010000])
    bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_5_XL, [0b01100100])
    bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_6_XL, [0b00100000])
    bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_7_XL, [0b00000000])
    bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_8_XL, [0b10100101])
    bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_9_XL, [0b00111000])
    bus.write_i2c_block_data(DEVICE_ADDRESS, CTRL_10_XL, [0b00111101])


    #Sorties accéléromètres
    ledout_values_x = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
    ledout_values_y = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]


    test = 0 #moyenne de C
    flag = 0 #flag choc

    #t_choc = 0
    #l_retour = [t_choc,flag]

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


    #Traitement des données des accéléromètres
    x-=173
    y+=212
    mx = np.abs(x)
    my = np.abs(y)
    test= mx+my

    
    #Détection du choc
    if test > 580:
        time.sleep(0.5)
        flag = 1
        #l_retour[0] = time.time()
        #l_retour[1] = flag
        return (flag)

