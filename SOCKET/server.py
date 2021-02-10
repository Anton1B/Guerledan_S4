import socket  # Import socket module
import matplotlib.pyplot as plt
from roblib_rob import *

port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.
s = socket.socket()  # Create a socket object
host = ""  # Get local machine name
# s.bind(('172.20.26.195', port))  # Bind to the port mon adresse ip
s.bind(('127.0.0.1', port)) # local
s.listen(5)  # Now wait for client connection.

print('Server listening....')

x = 0

fig, ax = plt.subplots(figsize = (8,7))
fig.canvas.set_window_title('Relevé coordonnées GPS')

while True:
    conn, address = s.accept()  # Establish connection with client.
    while True:
        try:
            print('Got connection from', address)
            data = conn.recv(1024)
            print('Server received : ', (data))
            x=(str(data)[3:-2]).split(",")
            [float(i) for i in x]
            print(x[0])
            print(type(float(x[1])))
            st = ('Thank you for connecting')
            byt = st.encode()
            conn.send(byt)

            # Plot data received data
            # ax.scatter((data),2,zorder=1, alpha= 0.2, c="b", s=10)
            pause(0.1)
            
        except Exception as e:
            print(e)
            break

conn.close()