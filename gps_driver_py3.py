import serial
import os
import time
import numpy as np
def latDD(y):
	D = int(y/100%100) #int(x[0:2])
	M = int((y-D*100)%100)
	S = int((y-D*100-M)*10000)
	DD = D +(float(M)+float(S)/10000)/60
	return DD

def longDD(y):
	if y != 0.0:
		D = int(y/100%100)	#int(x[0:1])
		M = int((y-D*100)%100)#int(x[1:3])
		S = int((y-D*100-M)*10000)#float(x[4:])
		DD = D +(float(M)+float(S)/10000)/60
		return -DD
	return 0

def init_line():
    ser = serial.Serial('/dev/ttyS0',timeout=1.0)
    time.sleep(1.0)
    print(ser)
    return ser

def read_gll(ser,nmax=20):
    val=[0.,'N',0.,'W',0.]

    for i in range(nmax):
        v=ser.readline().decode("utf-8")
        if str(v[0:6]) == "$GPGLL":
            vv = v.split(",")
            if len(vv[1]) > 0:
               val[0] = float(vv[1])
            if len(vv[2]) > 0:
                val[1] = vv[2]
            if len(vv[3]) > 0:
                val[2] = float(vv[3])
            if len(vv[4]) > 0:
                val[3] = vv[4]
            if len(vv[5]) > 0:
                val[4] = float(vv[5])
            break
    val[0] = latDD(val[0])
    val[2] = longDD(val[2])
    return val
   

def close(ser):
    ser.close()
