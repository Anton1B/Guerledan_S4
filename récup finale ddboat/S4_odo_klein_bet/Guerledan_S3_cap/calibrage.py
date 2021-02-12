import time
import smbus


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
dt = 10




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

    print(x,y,z)
    time.sleep(0.1)

