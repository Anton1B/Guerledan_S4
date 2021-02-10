# import socket  # Import socket module
# import os
# import re
# import time


# s = socket.socket()  # Create a socket object
# port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.

# # s.connect(('172.20.26.195', port)) # set ip adress to reach (your computer)

# s.connect(('127.0.0.1', port))
# x = 0

# st = str(x)
# byt = st.encode()
# s.send(byt)

# # send message 
# while True:
#     st = str(x)
#     byt = st.encode()
#     s.send(byt) 
#     while True:
#         data = s.recv(1024)
#         time.sleep(0.1)
#         if data:
#             print(data)
#             x += 1
#             break

#         else:
#             print('no data received')


# print('closing')
# s.close()


##

import socket
import time
from numpy import *


def send_msg(message):
    
    # message = (b'Hello, world')
    # print (b'Envoi de :' + message)
    n = client.send(message)
    if (n != len(message)):
            print ('Erreur envoi.')
    else:
            print ('Envoi ok.')

    # print ('Reception...')
    # donnees = client.recv(1024)
    # print ('Recu :', donnees)

    # print ('Deconnexion.')
    # client.close()

if __name__=="__main__":

    # Attempt connexion to server.
    try:
        HOST = ('127.0.0.1')
        PORT = 50000
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print ('Connexion vers ' + HOST + ':' + str(PORT) + ' reussie.')
    except ConnectionRefusedError:
        print ("Connexion impossible")

    for i in range(3):
        # X=array([[1],[2],[3]])
        X=(1,2,3,4)

        # Envoi du message
        try:
            send_msg(str(X).encode('utf-8'))
        except BrokenPipeError:
            pass
        time.sleep(1)