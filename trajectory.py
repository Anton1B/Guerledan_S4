from Myboat import bateau
import time

def triangle(bateau):
	t1 = time.time()
	while t1+20>time.time():
		bateau.regul_cap(120)
	while t1+40>time.time():
		bateau.regul_cap(240)
	while t1+60>time.time():
		bateau.regul_cap(0)
	bateau.set_speed(0,0)
	return True
	
	
def control_potentiel(phat,qhat,x) :
    px = x[0:2,:] #position du bateau

    nq = px - qhat #composante répulsive
    w = nq/(norm(nq)**3) - 2*(px-phat) #consigne

    psi_bar = arctan2(w[1,0],w[0,0])
    psi_bar = psi_bar*(180/pi) #conversion degrés
    return psi_bar
    
def waypoint(bateau,parcours) :
	point_id = 0
	n = len(parcours)-1 
	
	first_point = parcours[0]
	#Intitialisation des offsets
	offset_x = first_point[0,0]
	offset_y = first_point[1,0]
	
	t_init = time.time()
	
	while (True) :
	
		X_bateau = Myboat.state() #récupération de l'état du bateau

		#Détermination des points de la ligne actuelle
		if point_id-1 <0 :
			p1 = parcours[n]
		else :
			p1 = parcours[point_id-1]

		p2 = parcours[point_id]


		#Vecteur cons_b et a_b
		v_phatp2 = array([[p2[0,0]-pt_cons[0,0]],[p2[1,0]-pt_cons[1,0]]]) #vecteur phat-->p2
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
		if (p1[0,0] > p2[0,0]) :
			coef = (p1[1,0]-p2[1,0]) / (p1[0,0]-p2[0,0])
		else :
			coef = (p2[1,0]-p1[1,0]) / (p2[0,0]-p1[0,0])

		tf = (time.time()-t0) - t_init
		y = coef*tf #Fonction affine entre 2 points

		pt_cons = array([[tf+offset_x],[y+offset_y]])

		if p1[0,0] > p2[0,0] :
			phat = array([[offset_x-tf],[+offset_y-y]])


		u = control(pt_cons,pt_P,X_bateau) 

		Myboat.regul_cap(u)
	
	
