# client_python_tcp.py

# UCSB CS 176A Fall 2020 HW #1 Socket Programming
# Nicholas M Wong, PID: 3018439
# Syntax/libraries learned from geeksforgeeks.org, w3schools.com, docs.python.org

import socket
import sys

# Establish a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # AF_INET for ipv4 address family, SOCK_STREAM means TCP protocol
s.settimeout(0.5)   # Set time out for socket to 500 ms

# # Get user input for parameters
# host = input("Enter sever name or IP address: ")
# port = int(input("Enter port: "))
# if not(0 <= port <= 65535):
#     print("Invalid port number")
    
# command = input("Enter command: ")


# FORCED FOR TESTING
host = "localhost"
port = 12345
command = "ls"

# Try connecting to the server
try:
    s.connect( (host, port) )
# If socket.error is caught, then print an error
except socket.error as err:
    print("Could not connect to server.")
    sys.exit()

# Send command to the server
s.send( command.encode() )

# Receive the data (stdout from the command) from the server
dataFromServer = s.recv(1024)

# Store its contents in a file
f = open("client_tcp_stdout.txt", "w")
f.write( dataFromServer.decode() )
f.close()

# Print file saved
print("File ", "client_tcp_stdout.txt", " saved")

# Close the connection
s.close()