from roblib_rob import *
from numpy import linalg,transpose
import random
import matplotlib.pyplot as plt
# Données initiales
p1 = 1
p2 = 1
p3 = 0.1
dt = 0.05
largeur_piscine = 4*10
longueur_piscine = 5*10
#largeur_bateau  = 1 
#longueur_bateau = 3 

# Création du graphique
fig = figure(0)
ax=fig.add_subplot(111,aspect='equal')

def f(x,u1,u2):
    """
    Entrées: 
    x = np.array([[x1],[x2],[x3],[x4])
    u1 = 
    u2 = 
    """
    dx1=x[3,0]*cos(x[2,0])
    dx2=x[3,0]*sin(x[2,0])
    dx3=p1*(u1-u2)
    dx4=p2*(u1+u2)-p3*x[3,0]*abs(x[3,0])
    return array([[dx1],[dx2],[dx3],[dx4]])

def control(cap_desire,u,x):
    cap = cap_desire # cap desire
    cap_m = x[2,0]
    e = cap - cap_m
    A = array([[1,-1],[1,1]])
    A = linalg.inv(A)
    return 5*A@array([[sawtooth(e)],[1]])

def draw_pool(largeur_piscine,longueur_piscine):
    draw_box(ax,-largeur_piscine/2 , +largeur_piscine/2 ,-longueur_piscine/2,+longueur_piscine/2,col="darkblue")

def draw_boat(x):
    draw_tank(x,col='black',r=1,w=3)

def stop(u):
    u[1,0]=0
    u[0,0]=0
    return u

### SIMU
alpha = pi/2 # angle initial
x_boat = array([[0],[0],[0]])
x = array([[0],[0],[alpha],[0]])
u = array([[5],[5]])
for t in arange(0,20,dt):
    pause(0.001)
    cla()
    ax.set_xlim((-largeur_piscine/2)*1.1,+(largeur_piscine/2)*1.1)
    ax.set_ylim(-(longueur_piscine/2)*1.1,(longueur_piscine/2)*1.1)
    draw_pool(largeur_piscine,longueur_piscine)
    if x_boat[0,0] > 10:
        #u=stop(u)
        u = array([[0],[0]])
        x[3,0]=0
    else:
        u=control(pi/4,u,x)
    bruit = random.uniform(-pi/100,pi/100)
    x[2,0]+=bruit
    x=x+f(x,u[0,0],u[1,0])*dt
    # u=control(pi/4,u,x)
    x_boat=x[:3]
    print(x_boat[0,0])
    draw_boat(x_boat)

# cap = pi/4 # Cap désiré
# cap_m = x[2,0]
# e = cap - cap_m
# A = array([[1,-1],[1,1]])
# A = linalg.inv(A)
# print("A⁻1=",1)
# print("sawtooth=",sawtooth(e))
# print("[u1,u2]=",5*A@array([[sawtooth(e)],[1]]))


pause(10)