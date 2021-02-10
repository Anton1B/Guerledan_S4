
import numpy as np

RAYON_TERRE = 6371000 #m

# point référence en cartésien
LAT0 = (48.19906500)*2*np.pi/360
LONG0 = (-3.01473333)*2*np.pi/360

# point référence en degré décimal
LAT0_2 = (48.19906500)
LONG0_2 = (-3.01473333)

def xy_2_DD(x,y):
    ly = y/RAYON_TERRE + LAT0                   # latitude en DD !
    lx = x/(RAYON_TERRE * np.cos(ly)) + LONG0    # longitude en DD !
    return (ly*180/np.pi,lx*180/np.pi,)

def latDD(y):
	D = float(y/100%100) #int(x[0:2])
	M = float((y-D*100)%100)
	S = float((y-D*100-M)*10000)
	DD = D +(float(M)+float(S)/10000)/60
	return DD

def longDD(y):
	if y != 0.0:
		D = float(y/100%100)	#int(x[0:1])
		M = float((y-D*100)%100)#int(x[1:3])
		S = float((y-D*100-M)*10000)#float(x[4:])
		DD = D +(float(M)+float(S)/10000)/60
		return -DD
	return 0

def DD_2_cartesian(lat_DD,longi_DD):
    """
    Attention on est en degré décimal.
    """
    lat = lat_DD*2*np.pi/360
    longi = longi_DD*2*np.pi/360	
    x = RAYON_TERRE*np.cos(lat)*(longi-LONG0)
    y = RAYON_TERRE*(lat-LAT0)
    return (x,y)

if __name__=="__main__":

    # valeur en Degré minute - point au hasard (récupéré dans le log GPS)
    N = 4811.9363
    W = 300.8925
    print("Degré Minute",(N,W))

    # conversion en Degré décimal (DD)
    # 48.19893833333333 N, 3.0148733333333335 W
    N_DD = latDD(N)
    W_DD = longDD(W)
    print("Degré décimal",(N_DD,W_DD))

    # conversion en cartésien
    xy = DD_2_cartesian(N_DD,W_DD) # tuple
    print("Cartésien",xy)

    # back to DD (for visual representation)
    lxly = xy_2_DD(xy[0],xy[1])
    # lxly = xy_2_DD(5,5)
    print("Degré Décimal:",lxly)

    print(DD_2_cartesian(lxly[0],lxly[1]))