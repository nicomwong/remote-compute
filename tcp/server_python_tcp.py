# server_python_tcp.py

# UCSB CS 176A Fall 2020 HW #1 Socket Programming
# Nicholas M Wong, PID: 3018439
# Syntax/libraries learned from geeksforgeeks.org, w3schools.com, docs.python.org

import socket
import sys
import subprocess

# Check for valid cmd line input
if ( len(sys.argv) != 2):
    print("Usage: python server_python_tcp.py <port>")
    sys.exit()

# Set the port
port = int(sys.argv[1])
if not(0 <= port <= 65535):
    print("Invalid port number")

# Create the socket
s = socket.socket()

# Bind to this machine with the port
s.bind( ('', port) )

# Put the socket into listening mode
s.listen(5)

# Loop to wait for connections
while True:

    # Wait until a connection is received (blocking)
    c, addr = s.accept()

    # Try to receive the command
    try:
        commandFromClient = c.recv(1024)
    # If it times out, print an error and ditch the message
    except socket.timeout:
        print("Failed to receive instructions from the client.")
        break
    # Else, process the received commandFromClient
    else:
        # Run the command on the shell from server and store the output
        stdout = subprocess.check_output( commandFromClient.decode(), shell=True )

        # Put the output into a file
        f = open("server_tcp_stdout.txt", "w")
        f.write( stdout.decode() )
        f.close()

        # Send the file contents back to the client
        f = open("server_tcp_stdout.txt", "r")
        c.send( f.read().encode() )
        f.close()

        # Close the connection
        c.close()