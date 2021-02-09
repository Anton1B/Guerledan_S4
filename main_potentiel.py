from Myboat import bateau
import time
from roblib_rob import *

# def f1(phat,qhat,vhat,X1,X2):  
#     vhat = vhat.flatten()
#     phat = phat.flatten()

#     #consigne w(p,t) = -gradV(p) sans la composante répulsive
#     vx = 0*X1 +  vhat[0]-2*(X1-phat[0]) 
#     vy = 0*X2 + vhat[1]-2*(X2-phat[1])

#     #Composante répulsive
#     Nq1 = X1 - qhat[0]
#     Nq2 = X2 - qhat[1]

#     #Consigne complète
#     vx+= Nq1/((Nq1**2 + Nq2**2)**(3/2))
#     vy+= Nq2/((Nq1**2 + Nq2**2)**(3/2))

#     return vx,vy

def control(phat,qhat,x) :
    psi = x[2,0]
    px = x[0:2,:]

    nq = px - qhat #composante répulsive
    w = nq/(norm(nq)**3) - 2*(px-phat) #consigne

    psi_bar = arctan2(w[1,0],w[0,0])

    u2 = 10*arctan(tan((psi_bar-psi)/2)) #commande orientation

    u = u2
    return u


print("yo")
Myboat = bateau()

#Déclaration des points de parcours
pt_A = array([[1],[2]])
pt_B = array([[1],[2]])
pt_C = array([[1],[2]])

pt_cons = array([[0],[0]])

pt_P = array([[0],[0]])

#Parcours 
parcours = [pt_A,pt_B,pt_C]

pos_bateau = Myboat.get_gps()
psi_bateau = Myboat.cap()

X_bateau = vstack((pos_bateau,psi_bateau))
X_bateau = vstack((0))

n = 3 #nombre de points du parcours
t0 = 0

while (True) :
    #print(Myboat.cap())
    pos_bateau = Myboat.get_gps()
    psi_bateau = Myboat.cap()
    X_bateau = vstack((pos_bateau,psi_bateau))

    #Détermination des points de la ligne actuelle
    if int(X_bateau[3,0])-1 <0 :
        p1 = parcours[n]
    else :
        p1 = parcours[int(X_bateau[3,0])-1]

    p2 = parcours[int(X_bateau[3,0])]


    #Vecteur cons_b et a_b
    v_phatp2 = array([[p2[0,0]-pt_cons[0,0]],[p2[1,0]-pt_cons[1,0]]]) #vecteur phat-->p2
    v_p1p2 = array([[p2[0,0]-p1[0,0]],[p2[1,0]-p1[1,0]]]) #vecteur p1-->p2

    #test de changement de ligne
    dist_X = norm(v_phatp2) #distanc entre p1 et b

    #Si la cible est proche d'un point
    if dist_X < 1 :
        if X_bateau[3,0]+1 > n:
            X_bateau[3,0] = 0
        else : 
            X_bateau[3,0] += 1
        #Gestion des offsets
        t0 = time.time()
        offset_x = p2[0,0]
        offset_y = p2[1,0]


    if (p1[0,0] > p2[0,0]) :
        coef = (p1[1,0]-p2[1,0]) / (p1[0,0]-p2[0,0])

    else :
        coef = (p2[1,0]-p1[1,0]) / (p2[0,0]-p1[0,0])

    tf = time.time()-t0
    y = coef*tf

    pt_cons = array([[tf+offset_x],[y+offset_y]])

    if p1[0,0] > p2[0,0] :
        phat = array([[offset_x-tf],[+offset_y-y]])


    u = control(pt_cons,pt_P,X_bateau) 

    Myboat.regul_cap(u)
