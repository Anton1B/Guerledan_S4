import socket  # Import socket module
import os
import re
import time


s = socket.socket()  # Create a socket object
port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.

s.connect(('172.20.26.195', port))
x = 0

st = str(x)
byt = st.encode()
s.send(byt)

# send message 
while True:
    st = str(x)
    byt = st.encode()
    s.send(byt) 

    print(x)

    while True:
        data = s.recv(1024)
        time.sleep(0.1)
        if data:
            # print(data)
            x += 1
            break

        else:
            print('no data received')


print('closing')
s.close()
