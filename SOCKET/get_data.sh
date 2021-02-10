#!/bin/bash

while true; do
    rsync --rsh="sshpass -p ue32 ssh -l ue32" 172.20.25.210:S4_odo_klein_bet/Boat/mission1.csv /home/jvk/Bureau/Guerledan_S4/SOCKET
    if [ "$input" = "c" ]; then
        break
    fi
done 
