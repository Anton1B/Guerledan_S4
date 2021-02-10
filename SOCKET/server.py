import socket  # Import socket module
import matplotlib.pyplot as plt
from roblib_rob import *

port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.
s = socket.socket()  # Create a socket object
host = ""  # Get local machine name
s.bind(('localhost', port))  # Bind to the port
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
            print('Server received : ', float(data))
            st = ('Thank you for connecting')
            byt = st.encode()
            conn.send(byt)
            x += 1
            ax.scatter(float(data),2,zorder=1, alpha= 0.2, c="b", s=10)
            
            pause(0.1)
        except Exception as e:
            print(e)
            break

conn.close()