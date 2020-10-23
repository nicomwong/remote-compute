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

fileName = "server_tcp_stdout.txt"

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
        cmdFromClient = c.recv(1024)
    # If it times out, print an error and ditch the message
    except socket.timeout:
        print("Failed to receive instructions from the client.")
        break
    # Else, process the received cmdFromClient
    else:

        # Store command as str
        cmdStr = cmdFromClient.decode()

        notStdOut = False
        cmdList = []
        # Determine if the command format is of 'cmd > file'
        if '>' in cmdStr:
            notStdOut = True
            cmdList = cmdStr.split('>')
            fileSpecified = cmdList[1][1:]  # File name to the right of '>' w/o the first space
        
        # Run the command on the shell from server and store the output
        stdout = subprocess.check_output( cmdFromClient.decode(), shell=True )

        # Open the server file to write to
        f = open(fileName, "w")

        # If the output is in stdout, then write from stdout
        if notStdOut == False:
            f.write( stdout.decode() )
        # Else, write from the specified file
        else:
            fTemp = open(fileSpecified, "r")
            f.write( fTemp.read() )
            fTemp.close()

        # Close the file
        f.close()

        # Send the file contents back to the client
        f = open(fileName, "r")
        c.send( f.read().encode() )
        f.close()

        # Close the connection
        c.close()