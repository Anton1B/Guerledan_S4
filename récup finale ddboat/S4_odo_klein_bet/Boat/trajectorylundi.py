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
