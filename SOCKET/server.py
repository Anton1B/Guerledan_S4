import socket  # Import socket module
import matplotlib.pyplot as plt
from roblib_rob import *
from conversion_toolbox import *

port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.
s = socket.socket()  # Create a socket object
host = ""  # Get local machine name
s.bind(('172.20.26.195', port))  # Bind to the port mon adresse ip
# s.bind(('127.0.0.1', port)) # local
s.listen(5)  # Now wait for client connection.

print('Server listening....')

def map_base_nautique():
    # Creating new plot window.
    fig, ax = plt.subplots(figsize = (8,7))
    fig.canvas.set_window_title('Relevé coordonnées GPS')

    # Get OSM map tile and display it using matplotlib library
    BBox = ((-3.018064498901367,-3.013585209846497,48.19794588711593,48.19947447698833)) # define BBox, the area defined by the map.
    map = plt.imread("map.png")

    # Plot data.
    # ax.scatter(Y,X,zorder=1, alpha= 0.2, c="b", s=10)

    # Plot parameters.
    ax.set_title("Base nautique de Guerlédan")
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])

    ax.imshow(map, zorder=0, extent = BBox, aspect= "equal")
    return ax

ax = map_base_nautique()

# Plot reference point: bout du ponton
ax.scatter(-3.01473333,48.19906500, c="r", s=10) 

while True:
    conn, address = s.accept()  # Establish connection with client.
    while True:
        try:
            print('Got connection from', address)
            data = conn.recv(1024)
            print('Server received : ', data.decode())
            utf8 = data.decode()
            y = (utf8[1:-1]).split(",") # on se débarasse des crochets
            
            x_boat = float(y[0])
            y_boat = float(y[1])

            # Converting cartesian values to Decimal Degrees
            # for data representation
            x_target_cartesian=float(y[-2])
            y_target_cartesian=float(y[-1])
            # print(type(y_target_cartesian))
            x_target,y_target = xy_2_DD(x_target_cartesian,y_target_cartesian)
            
            # print(y_target,x_target)
            ax.scatter(y_boat,x_boat,zorder=1, alpha= 0.2, c="b", s=10)
            ax.scatter(y_target,x_target,zorder=1, alpha= 0.2, c="g", s=10)

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