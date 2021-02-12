import time
import sys
import gps_driver_py3 as gpsdrv
import csv

gps = gpsdrv.init_line()

def latDD(y):
    """
    JV Updated last Wed. 17:40
    Convert latitude DDM (degrees decimal minutes) to DD (decimal degrees).
    y = str or float.
    """
    x = str(y)
    D = float(x[0:2])
    d = float(x[2:])/60
    DD = D + d
    return DD

def longDD(y):
    """
    JV Updated last Wed. 17:40
    Convert longitude DDM (degrees decimal minutes) to DD (decimal degrees).
    y = str or float.
    """
    x = str(y)
    D = float(x[0:1])
    d = float(x[1:])/60
    DD = D + d
    return -DD # minus because West !

with open("data_gps2.csv","w") as csv_file:
    fieldnames=['x','y','z']
    writer=csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    while True:
        data = gpsdrv.read_gll(gps)
        print(data)
        writer.writerow({'x':latDD(data[0]),'y':longDD(data[2]),'z':data[4]})
        csv_file.flush()

gpsdrv.close(gps)
csv_file.close()