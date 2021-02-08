from roblib_rob import *
from numpy import linalg,transpose
import random

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
    """
    dx1=x[3,0]*cos(x[2,0])
    dx2=x[3,0]*sin(x[2,0])
    dx3=p1*(u1-u2)
    dx4=p2*(u1+u2)-p3*x[3,0]*abs(x[3,0])
    return array([[dx1],[dx2],[dx3],[dx4]])

# def detect_choc(x):
#     """
#     Detection de chocs
#     """
#     flag=False

#     if (x[0,0]>=5 and flag==False):
#         # on a un choc
#         flag=True
#         return control(cap+pi/2,x)
#     return control(cap,x)
    
#     # if x[0,0]<5:
#     #     flag=True

def detect_choc(cap,x,flag):
    global nb_choc
    nb_choc_test = nb_choc
    if x[0,0]>=10:
        nb_choc+=1                # 1 choc en plus
        x[0,0] = 4                # choc qui va pousser la bateau en arriere
       
        # if flag==False:         # le drapeau est baissé, on peut y aller
        #     flag=True           # on remonte le drapeau pour executer qu'une seule fois
        #     cap = cap + pi/2    # 
        # flag = True             # le drapeau est levé on ne rentre pas dans le changement de cap     

    if nb_choc_test == (nb_choc-1):
        print(True)

        return (cap + pi)
    else:
    #print(nb_choc,nb_choc_test)
        return cap+pi/4         

def cap(cap,x):
    flag = False
    print(nb_choc)
    return control(detect_choc(cap,x,flag),x)

def control(cap_desire,x):
    cap_m = x[2,0]
    e = cap_desire - cap_m
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

### SIMULATION ###
alpha = pi/2 # angle initial
x_boat = array([[0],[0],[0]])
x = array([[0],[-longueur_piscine/2+3],[alpha],[0]])
u = array([[5],[5]])
cap_desire0 = 0
nb_choc = 0

for t in arange(0,20,dt):
    pause(0.001)
    cla()
    ax.set_xlim((-largeur_piscine/2)*1.1,+(largeur_piscine/2)*1.1)
    ax.set_ylim(-(longueur_piscine/2)*1.1,(longueur_piscine/2)*1.1)
    draw_pool(largeur_piscine,longueur_piscine)
    u = cap(cap_desire0,x)
    bruit = random.uniform(-pi/100,pi/100)
    x[2,0]+=bruit
    x=x+f(x,u[0,0],u[1,0])*dt
    x_boat=x[:3]
    draw_boat(x_boat)
pause(10)