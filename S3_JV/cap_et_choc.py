import time
import arduino_driver_py3 as ardudrv
import numpy as np
import fonction_regul_cap as cap
import fonction_detection_choc as choc


def sawtooth(x):
    return ((x+np.pi)%(2*np.pi))-np.pi   # or equivalently   2*arctan(tan(x/2))

p1 = 1
p2 = 1
p3 = 0.1
dt = 0.05

cmdl = 150
cmdr = 150
u = np.array([[cmdr],[cmdl]])
tour = 0

def control(cap_desire,tour):
    cap_m0 = cap.get_cap()+tour*360
    cap_m = cap_m0*np.pi/180
    e = cap_desire-cap_m
    #print(cap_m0)
    # print(cap_desire*180/np.pi,cap_m*180/np.pi,e,sawtooth(e))
    A = np.array([[0.5,0.5],[-0.5,0.5]])

    return 150*A@np.array([[sawtooth(e*0.6)],[1]])

def control_choc(cap_desire,tour):
    cap_m0 = cap.get_cap()+tour*360
    cap_m = cap_m0*np.pi/180
    e = cap_desire-cap_m
    #print(cap_desire*180/np.pi,cap_m0)
    A = np.array([[0.5,0.5],[-0.5,0.5]])

    return 100*A@np.array([[sawtooth(e*0.5)],[1]])

def control_choc_2pi(cap_desire,tour):
    cap_m0 = cap.get_cap()+tour*360
    cap_m = cap_m0*np.pi/180
    e = cap_desire-cap_m
    if e > 100*(np.pi/180) :
        e = -((360*np.pi/180)-e)
    #print(cap_desire*180/np.pi,cap_m0)
    A = np.array([[0.5,0.5],[-0.5,0.5]])
    return 100*A@np.array([[sawtooth(e*0.5)],[1]])

# INITIALISATION MOTEURS
duration = 60.0
serial_arduino, data_arduino = ardudrv.init_arduino_line()
timeout = 1.0
data_arduino = ardudrv.get_arduino_status(serial_arduino,timeout)
t0 = time.time()

cap_actuel = 90*(np.pi/180)

flag2pi = 0
while (time.time()-t0) < duration:
    #print(tour)
    
    if flag2pi ==1 :
        flag2pi = 0
        tour+=1
    
    u=np.abs(control(cap_actuel,tour))
    ardudrv.send_arduino_cmd_motor(serial_arduino,u[0,0]*0.5,u[1,0])    

    print(cap.get_cap()+tour*360,cap_actuel*180/np.pi)

    flag =0
    #l_retour = choc.get_choc()
    #t1 = l_retour[0]
    #flag = l_retour[1]
    flag = choc.get_choc()
    #print(flag)
    #print(cap_actuel*(180/np.pi))
    if flag == 1 :
        #print(cap_actuel*(180/np.pi))
        cap_actuel += np.pi/2
        flag = 0
        time.sleep(1)
        cap_m_t = cap.get_cap()+tour*360
        #print(cap_actuel%(2*np.pi))
        if round(cap_actuel%(2*np.pi)) == 0 :
            flag2pi = 0
            while cap_m_t <= cap_actuel*180/np.pi:

                print(cap.get_cap()+tour*360,cap_actuel*180/np.pi)

                cap_m_t = cap.get_cap()+tour*360
                u=np.abs(control_choc_2pi(cap_actuel,tour))
                ardudrv.send_arduino_cmd_motor(serial_arduino,u[0,0],u[1,0]) 
                if choc.get_choc() ==1 and (cap_m_t>350 or cap_m_t <200):
                    break

                # cap_m = cap_m_t*np.pi/180
                # e = cap_actuel-cap_m
                # if e > 100*(np.pi/180) :
                #     e = -((360*np.pi/180)-e)
                #print(cap_m_t+tour*360," ",cap_actuel*180/np.pi,tour)
                
                #     ardudrv.send_arduino_cmd_motor(serial_arduino,0,0)
                #     time.sleep(2)
                #     break
            flag2pi = 1
        else :
            while cap_m_t <= (cap_actuel*180/np.pi) :
                cap_m_t = cap.get_cap()+tour*360

                print(cap.get_cap()+tour*360,cap_actuel*180/np.pi)

                #print(cap_m_t+tour*360," ",cap_actuel*180/np.pi)
                u=np.abs(control_choc(cap_actuel,tour))
                ardudrv.send_arduino_cmd_motor(serial_arduino,u[0,0]*0.75,u[1,0])
        

    
        
    
    

# ARRETS MOTEURS
cmdl = 0
cmdr = 0
ardudrv.send_arduino_cmd_motor(serial_arduino,cmdl,cmdr)