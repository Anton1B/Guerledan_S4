
def diffAngle(angle1,angle2):
	diff = angle1 - angle2 
	return mod(diff+np.pi,2*np.pi)-np.pi

def asservit(angle):
	angle-=terme*capteur.get_rot()
	D,G=1,1
	ouverture = 25*np.pi/180
	G = 0.5*(ouverture+angle)/ouverture
	D=1-G
	if abs(angle)>ouverture:
		if angle<0:
			G = 0
			D = 1
		else:
			G = 1
			D = 0
	return D**0.5,G**0.5

def get_angle(vect):
	vect = vect/np.linalg.norm(vect)
	angle = np.arccos(vect[1])
	if vect[0]>0:
		angle=2*np.pi-angle
	return angle
	

orientation = capteur.get_CapF()
direction = "cap rechercher"
angle = diffAngle(direction,orientation)
D,G = asservit(angle)
commande.set(G*maximum*power,D*maximum*power)
