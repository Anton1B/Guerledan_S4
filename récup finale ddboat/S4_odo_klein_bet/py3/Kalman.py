import numpy as np
import time

def kalman_predict(xup,Gup,u,Γα,A):
    Γ1 = A @ Gup @ A.T + Γα
    x1 = A @ xup + u    
    return(x1,Γ1)    

def kalman_correc(x0,Γ0,y,Γβ,C):
    S = C @ Γ0 @ C.T + Γβ        
    K = Γ0 @ C.T @ np.linalg.inv(S)           
    ytilde = y - C @ x0        
    Gup = (np.eye(len(x0))-K @ C) @ Γ0 
    xup = x0 + K@ytilde
    return(xup,Gup) 
    
def kalman(x0,Γ0,u,y,Γα,Γβ,A,C):
    xup,Gup = kalman_correc(x0,Γ0,y,Γβ,C)
    x1,Γ1=kalman_predict(xup,Gup,u,Γα,A)
    return(x1,Γ1) 

class Kalman:
	def __init__(self):
		self.X = np.array([])
		self.Gx= np.array([])
		self.first = True
		self.C = np.array([[1.,0,0],[0,1,0]])
		self.Gbeta=np.array([[25.,0],[0,25]])
		self.Galpha= np.array([[0.01,0,0],[0,0.01,0],[0,0,1]])
		self.u = np.array([[0.,0,0]]).T
		self.X = np.array([[0.,0,0]]).T
		self.cap = 0
		self.temps = time.time()
		
	def integre1(self,cap,pos):
		self.cap = cap
		newTime = time.time()
		if self.first:
			self.first = False
			self.X = np.array([[pos[0],pos[1],0]]).T
			self.Gx= np.array([[25.,0,0],[0,25.,0],[0,0,1]])
		else:
			dt = newTime - self.temps
			Ak = np.array([[1,0,-dt*np.sin(cap)],[0,1,dt*np.cos(cap)],[0,0,1]])
			y = np.array([[pos[0],pos[1]]]).T
			self.X,self.Gx=kalman(self.X,self.Gx,self.u,y,self.Galpha,self.Gbeta,Ak,self.C)
		self.temps = newTime
	
	def get_last(self):
		return np.array([self.X[0,0],self.X[1,0]])
	
	def get_vit(self):
		return self.X[2,0]
	
	def get_sim(self):
		dt = time.time() - self.temps
		return np.array([self.X[0,0]-self.X[2,0]*dt*sin(self.cap),self.X[1,0]+self.X[2,0]*dt*cos(self.cap)])
			
		
