from Myboat import bateau,sawtooth
import time
from numpy import array,arctan2,pi,arctan,tan
from numpy.linalg import norm
class trajectory():
	def __init__(self):
		self.pt_cons = array([[0],[0]])

	def triangle(self,bateau):
		t1 = time.time()
		self.pt_cons = array([[0],[0]])
		while t1+20>time.time():
			control(bateau,2*pi/3,50)
		while t1+40>time.time():
			control(bateau,4*pi/3,50)
		while t1+60>time.time():
			control(bateau,0,50)
		bateau.set_speed(0,0)
		return True

	def waypoint2(self,Myboat,parcours,vo):
		#On suppose vo = 1 m.s-1 pour les hélices à 80 de forces
		def f(t,xo,yo,a,b):
			return array([[xo + t*a],[yo+t*b]])
		def determine_a_b(p_i,p_f,vo):
			d = norm(p_f-p_i)
			a = (p_f[0,0]-p_i[0,0])*vo/d
			b = (p_f[1,0]-p_i[1,0])*vo/d
			return a,b
		to = time.time()
		i_p = 1
		p_i = parcours[0]
		p_f = parcours[1]
		a,b = determine_a_b(p_i,p_f,vo)
		vhat = array([[a*vo/((a**2+b**2)**(1/2))],[b*vo/((a**2+b**2)**(1/2))]])
		print("a = ", a)
		print("b = ", b)
		print("vhat = ",vhat)
		self.pt_cons = f(0,p_i[0,0],p_i[1,0],a,b)
		while True:
			if norm(self.pt_cons-p_f) <0.5:
				p_i = p_f
				i_p +=1
				p_f = parcours[i_p%len(parcours)]
				a,b = determine_a_b(p_i,p_f,vo)
				vhat = array([[a*vo/((a**2+b**2)**(1/2))],[b*vo/((a**2+b**2)**(1/2))]])
				print("a = ", a)
				print("b = ", b)
				print(vhat)
				to = time.time()
			self.pt_cons = f(time.time()-to,p_i[0,0],p_i[1,0],a,b)
			X_bateau = array([[Myboat.x],[Myboat.y]])
			v,psi_bar = guidage_v2(pt_con,array([[-2],[-2]]),X_bateau,vhat)
			control_v2(Myboat,psi_bar,v)
			print("ecart" , self.pt_cons - X_bateau[0:2,:])
			print("X_bateau" ,X_bateau[0:2,:])
			print("CONSIGNE" , self.pt_cons)
	
			
			
		
	def unpoint(self,Bateau,point):
		while True :
			X_Bateau = array([[Bateau.x],[Bateau.y]])
			v,psi_bar = guidage(Bateau,point,array([[0],[1]]),X_Bateau,0)
			control(Bateau,psi_bar,v) 
			#print("ecart" , point - X_Bateau[0:2,:])
			
	def unpoint_v2(self,Bateau,point):
		while True :
			X_Bateau = array([[Bateau.x],[Bateau.y]])
			v,psi_bar = guidage_v2(point,array([[0],[1]]),X_Bateau,1)
			control_v2(Bateau,psi_bar,v) 
			print("ecart" , point - X_Bateau[0:2,:])
			
	def waypoint(self,Myboat,parcours,vo) :
		#pour vo = 160
		point_id = 1
		n = len(parcours)-1 
		
		first_point = parcours[0]
		#Intitialisation des offsets
		offset_x = first_point[0,0]
		offset_y = first_point[1,0]
		
		t_init = time.time()
		pt_P = array([[0],[0]])
		self.pt_cons = array([[0],[0]])
		t0 = time.time()
		sign = 1
		while (True) :
			X_bateau = array([[Myboat.x],[Myboat.y]]) #récupération de l'état du bateau
			#Détermination des points de la ligne actuelle
			if point_id == 0:
				p1 = parcours[n]
			else :
				p1 = parcours[point_id-1]

			p2 = parcours[point_id]


			#Vecteur cons_b et a_b
			v_phatp2 = array([[p2[0,0]-self.pt_cons[0,0]],[p2[1,0]-self.pt_cons[1,0]]]) #vecteur phat-->p2
			v_p1p2 = array([[p2[0,0]-p1[0,0]],[p2[1,0]-p1[1,0]]]) #vecteur p1-->p2

			#test de changement de ligne
			dist_X = norm(v_phatp2) #distanc entre p1 et b

			#Si la cible est proche d'un point
			if dist_X < 1 :
				if point_id+1 > n:
				    point_id = 0
				else : 
				    point_id += 1
				#gestion des offsets
				t0 = time.time()
				offset_x = p2[0,0]
				offset_y = p2[1,0]

			#Calcul du coefficient directeur
			coef = (p1[1,0]-p2[1,0]) / (p1[0,0]-p2[0,0])
			tf = (time.time()-t0)# - t_init
			 #Fonction affine entre 2 points
			if p1[0,0] > p2[0,0] :
				sign = -1
			else :
				sign = 1
			y = sign*coef*tf
			self.pt_cons = array([[sign*tf+offset_x],[y+offset_y]])
			#print("CONSIGNE", self.pt_cons)
			#print("POSBATO", X_bateau)
			print("ecart" , self.pt_cons - X_bateau[0:2,:])
			
			vo = v_p1p2
			v_cons,psi_bar = guidage(Myboat,self.pt_cons,pt_P,X_bateau,vo) 
			control(Myboat,psi_bar,v_cons)

			# log data
		
		
def guidage(Myboat,phat,qhat,x,vo) :
    px = x[0:2,:] #position du bateau

    nq = px - qhat #composante répulsive
    w = -0.1*(px-phat) + vo #consigne
    #print("w : ",w)
    vbar = norm(w) 
    psi_bar = arctan2(w[1,0],w[0,0])
    #if psi_bar<0:
    #	psi_bar = 2*pi+psi_bar
    
    v_phatbateau = array([[x[0,0]-phat[0,0]],[x[1,0]-phat[1,0]]])
    
    #v = Myboat.u1 + Myboat.u2
    
    v_cons = norm(v_phatbateau)*vbar/norm(vo+0.1) #- v
    
    #print("psi_bar",psi_bar)
    #print("v_cons : ",v_cons)
    return v_cons,psi_bar

def guidage_v2(phat,qhat,x,vo) :
    px = x[0:2,:] #position du bateau

    nq = px - qhat #composante répulsive
    w = nq/(norm(nq)**3) - 0.01*(px-phat) + vo #consigne
    v = norm(w)
    psi_bar = arctan2(w[1,0],w[0,0])
    if psi_bar<0:
    	psi_bar = 2*pi+psi_bar
    return v,psi_bar

def control_v2(Myboat,psi_bar,v):
    u2 = min(v*160,240)
    u1 = 10*arctan(tan((Myboat.cap()-psi_bar)/2))
    Myboat.set_speed((u2-u1)/2,(u2+u1)/2)

def control(Myboat,psi_bar,v_cons) :
    u2 = min(v_cons*0, 240) #vitesse
    ul,ur = Myboat.regul_cap_lundi(0)
    #print("ul-ur",ul," ",ur)
    p1 = ul + u2
    p2 = ur + u2
    
    #print("p1 : ", p1)
    #print("p2 : ", p2)
    
    print("psibar ", psi_bar)
    
    #u1 = 20*arctan(tan((psi_bar-Myboat.cap())/2)) #orientation
    #p1 = int((u2-u1)*0.5)
    #p2 = int((u2+u1)*0.5)
    
    Myboat.set_speed(p2,p1)

	
	
