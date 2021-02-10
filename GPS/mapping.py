"""
Permet de convertir les données brutes du capteur GPS et les affiche avec Matplotlib.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv 
from roblib_rob import *

import random

import socket  # Import socket module
import os
import re
import time


X=[]
Y=[]
Z=[]

# lien intéressant conversion des données
# https://www.pgc.umn.edu/apps/convert/

# Opening socket
s = socket.socket()  # Create a socket object
port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.

s.connect(('172.20.26.195', port)) # set ip adress to reach (your computer)
t = 0

st = str(t)
byt = st.encode()
s.send(byt)

def latDD(y):
    """
    Convert latitude DDM (degrees decimal minutes) to DD (decimal degrees).
    """
    x=(y)
    D=int(x[0:2])
    M=int(x[2:4])
    S=float(x[5:])
    DD = D +(float(M)+float(S)/10000)/60
    return DD

def longDD(y):
    """
    Convert longitude DDM (degrees decimal minutes) to DD (decimal degrees).
    """
    x=(y)
    D=int(x[0:1])
    M=int(x[1:3])
    S=float(x[4:])
    DD = D +(float(M)+float(S)/10000)/60
    return -DD*correction

correction = 1
# correction = np.cos(48*np.pi/180) A REVOIR AVEC YOHANN

with open("History/gps-0902-guerledan.csv","r") as csv_file: # read csv file: GPS log. 
    csv_reader = csv.reader(csv_file,delimiter=",")
    for lines in csv_reader:
        if float(lines[0])!=0.0:
            X.append(latDD(lines[0]))  # store lattitude in X to plot 
        if float(lines[1])!=0.0:
            Y.append(longDD(lines[1])) # store longitude in Y to plot

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

# ax = map_base_nautique()

# Plot reference point: bout du ponton
# ax.scatter(-3.01473333*correction,48.19906500, c="r", s=10) 
print(X[-1],Y[-1])

# Progressive ploting
# for t in np.arange(0,1000,1):
while True:
    # ax.scatter(Y[t],X[t],zorder=1, alpha= 0.2, c="b", s=10)
    st = str(Y[t])
    byt = st.encode()
    s.send(byt) 
    # while True:
    data = s.recv(1024)
    time.sleep(0.1)
    if data:
        # print(data)
        t += 1
        break
    else:
        print('no data received')
    plt.pause(0.001)

plt.show()