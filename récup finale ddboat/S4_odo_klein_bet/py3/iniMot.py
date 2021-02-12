from motor_py3 import *
import arduino_driver_py3 as ard

serial_arduino, data_arduino = ard.init_arduino_line()

pas = int(input("Pas : "))
commande = Commande(serial_arduino,True,pas)

print("over")