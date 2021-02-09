"""
Permet de convertir les données brutes du capteur GPS et les affiche avec Matplotlib.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv 
from roblib_rob import *
import os

import random

X=[]
Y=[]
Z=[]

# lien intéressant conversion des données
# https://www.pgc.umn.edu/apps/convert/

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

correction = 1
# correction = np.cos(48*np.pi/180) A REVOIR AVEC YOHANN

# Reading all file.
# with open("data_gps2.csv","r") as csv_file: # read csv file: GPS log. 
    # csv_reader = csv.reader(csv_file,delimiter=",")
    # print(csv_reader)
    # for lines in csv_reader:
        # if float(lines[0])!=0.0:
        #     X.append(latDD(lines[0]))  # store lattitude in X to plot 
        # if float(lines[1])!=0.0:
        #     Y.append(longDD(lines[1])) # store longitude in Y to plot

def get_last_line_csv():

    # Update last file from boat
    os.system('rsync --rsh="sshpass -p ue32 ssh -l ue32" 172.20.25.210:S4_odo_klein_bet/GPS/data_gps2.csv /home/jvk/Bureau/Guerledan_S4/SOCKET')
    os.system('sleep $1')
    with open("/home/jvk/Bureau/Guerledan_S4/SOCKET/data_gps2.csv","r") as csv_file: # read csv file: GPS log. 
        data = csv_file.readlines() 
    lastRow = data[-1] 
    lastRow = lastRow.split(",")
    return latDD(float(lastRow[0])),longDD(float(lastRow[1]))

def map_base_nautique():
    # Creating new plot window.
    fig, ax = plt.subplots(figsize = (8,7))
    fig.canvas.set_window_title('Relevé coordonnées GPS')

    # Get OSM map tile and display it using matplotlib library
    BBox = ((-3.018064498901367*correction,-3.013585209846497*correction,48.19794588711593,48.19947447698833)) # define BBox, the area defined by the map.
    map = plt.imread("map.png")

    # Plot data.
    # ax.scatter(Y,X,zorder=1, alpha= 0.2, c="b", s=10)

    # Plot parameters.
    ax.set_title("Base nautique de Guerlédan")
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])

    ax.imshow(map, zorder=0, extent = BBox, aspect= "equal")
    return ax

ax = map_base_nautique()

# Plot reference point: bout du ponton
ax.scatter(-3.01473333*correction,48.19906500, c="r", s=10) 

# Progressive ploting
while True:
    data_xy = get_last_line_csv()
    print(data_xy)
    ax.scatter(data_xy[1],data_xy[0],zorder=1, alpha= 0.2, c="b", s=10)
    plt.pause(0.001)

plt.show()