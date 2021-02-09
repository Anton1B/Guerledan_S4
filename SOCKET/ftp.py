from ftplib import FTP
ftp = FTP("172.20.25.210","ue32","ue32")  # connect to host, default port
# ftp.login(user="ue32",passwd="ue32")                     # user anonymous, passwd anonymous@
# ftp.cwd('')               # change into "debian" directory
# ftp.retrlines('LIST')           # list directory contents