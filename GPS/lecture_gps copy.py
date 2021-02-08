import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv 

X=[]
Y=[]
Z=[]

def latDD(y):
    x=(y)
    D=int(x[0:2])
    M=int(x[2:4])
    S=float(x[5:])
    DD = D +(float(M)+float(S)/10000)/60
    return DD

def longDD(y):
    x=(y)
    D=int(x[0:1])
    M=int(x[1:3])
    S=float(x[4:])
    DD = D +(float(M)+float(S)/10000)/60
    return -DD*np.cos(48*np.pi/180)

with open("data_gps2.csv","r") as csv_file: # autre = data_r_gps.csv
    csv_reader = csv.reader(csv_file,delimiter=",")

    for lines in csv_reader:
        if float(lines[0])!=0.0:
            X.append(latDD(lines[0]))  # LATITUDE
        if float(lines[1])!=0.0:
            Y.append(longDD(lines[1])) # LONGITUDE

BBox = ((-4.47460*np.cos(48*np.pi/180),-4.47095*np.cos(48*np.pi/180),48.41739,48.41931))
# ensta = plt.imread("map.png")
fig, ax = plt.subplots(figsize = (8,7))
fig.canvas.set_window_title('Relevé coordonnées GPS')
#ax = plt.subplot()
ax.scatter(Y,X,zorder=1, alpha= 0.2, c="b", s=10)
#ax.plot(Y[:200],X[:200])
ax.set_title("Campus ENSTA Bretagne")
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
# ax.imshow(ensta, zorder=0, extent = BBox, aspect= "equal")
plt.show()

print(X[-1],Y[-1])