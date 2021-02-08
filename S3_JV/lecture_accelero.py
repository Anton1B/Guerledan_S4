import csv
import matplotlib.pyplot as plt
import numpy as np
import time

def av(X) :
    somme = 0
    for i in X :
        somme+=i
    return somme/len(X)


X = []
Y = []
T = []

C = []

with open("data_acc.csv","r") as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=",")
    for lines in csv_reader:
        X.append(float(lines[0]))
        Y.append(float(lines[1]))
        T.append(float(lines[2]))


Z = []
test = 0
nb_chocs = 0
ecart = 0 
flag = 0
t1=0
for i in range (len(X)):
    X[i]-=173
    Y[i]+=212
    x = np.abs(X[i])
    y = np.abs(Y[i])
    Z.append(x**2+y**2)
    C.append(x**2+y**2)
    if len(C)>100:
        test = av(C)
        C.pop(0)
    
    if test > 10000 and flag==0:
        t1 = T[i]
        flag = 1
    if T[i]-t1 >1 :
        t1=10000
        nb_chocs+=1
        flag = 0

print(nb_chocs)
        
    



# plt.plot(T,X, label='acc x')
# plt.plot(T,Y,label='acc y')
plt.plot(T,Z,label='mix acc')

plt.legend()

plt.show()