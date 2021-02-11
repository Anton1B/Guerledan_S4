import time
import arduino_driver_py3 as ardudrv
import numpy as np


cmdl = 20
cmdr = 20
u = np.array([[cmdr],[cmdl]])

# INITIALISATION MOTEURS
duration = 5.0
serial_arduino, data_arduino = ardudrv.init_arduino_line()
timeout = 1.0
data_arduino = ardudrv.get_arduino_status(serial_arduino,timeout)
t0 = time.time()

# FONCTIONNEMENT DES MOTEURS
while (time.time()-t0) < duration:
    # u=np.abs(control(80*(np.pi/180)))
    ardudrv.send_arduino_cmd_motor(serial_arduino,u[0,0],u[1,0]+20)
    
# ARRETS MOTEURS
cmdl = 0
cmdr = 0
ardudrv.send_arduino_cmd_motor(serial_arduino,cmdl,cmdr)