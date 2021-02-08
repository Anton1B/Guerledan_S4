import csv
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
import numpy as np

X = []
Y = []
Z = []
with open("/home/ut/Desktop/data.csv","r") as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=",")
    for lines in csv_reader:
        X.append(float(lines[0]))
        Y.append(float(lines[1]))
        Z.append(float(lines[2]))

## Affichage de l'Ellipse
def dessin(X,Y,Z):
    ellipse = plt.figure()
    ax = ellipse.add_subplot(111, projection='3d')
    ax.scatter(X,Y,Z)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()

## Centrage
def av(X):
    x=max(X)
    y=min(X)
    return (x+y)/2

def transl(X):
    X2=[]
    m=av(X)
    for i in X:
        i+=-m
        X2.append(i)
    return X2

X2=transl(X)
Y2=transl(Y)
Z2=transl(Z)

#print(av(X2),av(Y2),av(Z2))
#dessin(X,Y,Z)
#dessin(X2,Y2,Z2)

# print(av(X))
# print(av(Y))
# print(av(Z))

# Trouver les parametres

#p0 = np.array([[av(X)],[av(Y)],[av(Z)],[1/max(X)],[1/max(Y)],[1/max(Z)],[0],[0],[0]]) # forme une matrice identité
p0 = np.array([[av(X)],[av(Y)],[av(Z)],[1/3000],[1/3000],[1/3000],[0],[0],[0]]) # forme une matrice identité

def fp(x,p0):
    I1 = np.array([[p0[3,0],p0[6,0],p0[8,0]],
              [p0[6,0],p0[4,0],p0[7,0]],
              [p0[8,0],p0[7,0],p0[5,0]]])
    I2 = np.array([[p0[0,0]],[p0[1,0]],[p0[2,0]]])
    return I1 @ (x-I2)

X3=[]
Y3=[]
Z3=[]
N=np.array([[0],[0],[0]])
with open("/home/ut/Desktop/data.csv","r") as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=",")
    for lines in csv_reader:
        #print(lines)
        N[0,0]=float(lines[0]) #X
        N[1,0]=float(lines[1]) #Y
        N[2,0]=float(lines[2]) #Z
        N2 = fp(N,p0)
        X3.append(N2[0,0])
        Y3.append(N2[1,0])
        Z3.append(N2[2,0])
        #print(N2)
        #test = fp(lines,p0)
dessin(X3,Y3,Z3)

# print(av(X))
# print(av(Y))
# print(av(Z))

# print(max(X))
# print(max(Y))
# print(max(Z))

# def j(x,p0):
#     s = 0 # somme
#     for i in range(len(x)):
#         sum+=pow(np.abs(fp(x,p0))-1,2)       