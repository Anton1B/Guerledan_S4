import time
import sys
import gps_driver_py3 as gpsdrv
import csv

gps = gpsdrv.init_line()

with open("data_gps2.csv","w") as csv_file:
    fieldnames=['x','y','z']
    writer=csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    while True:
        data = gpsdrv.read_gll(gps)
        print(data)
        writer.writerow({'x':data[0],'y':data[2],'z':data[4]})

gpsdrv.close(gps)
csv_file.close()