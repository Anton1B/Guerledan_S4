import time
import arduino_driver_py3 as ardudrv
import numpy as np
import fonction_regul_cap as cap


def sawtooth(x):
    return ((x+np.pi)%(2*np.pi))-np.pi   # or equivalently   2*arctan(tan(x/2))

p1 = 1
p2 = 1
p3 = 0.1
dt = 0.05

cmdl = 20
cmdr = 20
u = np.array([[cmdr],[cmdl]])

def control(cap_desire):
    cap_m = cap.get_cap()*np.pi/180
    e = cap_desire-cap_m
    print(cap.get_cap())
    A = np.array([[0.5,0.5],[-0.5,0.5]])
    #A = np.linalg.inv(A)
    #print(sawtooth(e))
    return 100*A@np.array([[sawtooth(e*0.5)],[1]])

# INITIALISATION MOTEURS
duration = 60.0
serial_arduino, data_arduino = ardudrv.init_arduino_line()
timeout = 1.0
data_arduino = ardudrv.get_arduino_status(serial_arduino,timeout)
t0 = time.time()

# FONCTIONNEMENT DES MOTEURS
while (time.time()-t0) < duration:
    u=np.abs(control(80*(np.pi/180)))
    ardudrv.send_arduino_cmd_motor(serial_arduino,u[0,0],u[1,0]+20)

# ARRETS MOTEURS
cmdl = 0
cmdr = 0
ardudrv.send_arduino_cmd_motor(serial_arduino,cmdl,cmdr)