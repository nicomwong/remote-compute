# client_python_udp.py

# UCSB CS 176A Fall 2020 HW #1 Socket Programming
# Nicholas M Wong, PID: 3018439
# Syntax/libraries learned from geeksforgeeks.org, w3schools.com, docs.python.org

import socket
import sys

# Establish a socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # AF_INET for ipv4 address family, SOCK_DGRAM means UDP protocol

# # Get user input for parameters
# serverAddr = input("Enter sever name or IP address: ")
# port = int(input("Enter port: "))
# if not(0 <= port <= 65535):
#     print("Invalid port number")
    
# command = input("Enter command: ")

# serverAddr = (host, port)


# FORCED FOR TESTING
host = "localhost"
port = 12345
command = "echo hello server"

serverAddr = (host, port)

# Send length of command to the server

ackNotReceived = True
timeoutCount = 0

while (ackNotReceived and timeoutCount < 3):

    # Send the command length to the server
    s.sendto( str( len(command) ).encode(), serverAddr)

    # Send the command to the server
    s.sendto(command.encode(), serverAddr)

    # Set socket timeout to 1 s
    s.settimeout(1)

    # Wait for an ACK to be received
    try:
        ack, addr = s.recvfrom(1024)
    # If it times out, resend length and command
    except socket.timeout:
        timeoutCount += 1
        continue
    # Else, if the message is ACK, then set ack to received
    else:
        if ack.decode() == "ACK":
            ackNotReceived = False
        
# If timeoutCount reached 3, then print failure and terminate
if timeoutCount >= 3:
    print("Failed to send command. Terminating.")
    sys.exit()

# If ACK was received, then print that
if ackNotReceived == False:
    print("received ACK")

# Try to receive the message length
try:
    # Receive the expected message length from the server
    data, addr = s.recvfrom(1024)
    expectedLength = int( data.decode() )
    print("Expected length =", expectedLength)

# If it times out, print an error and stop
except socket.timeout:
    print("Failed to receive command output from server in time")
    sys.exit()

# At this point, the length message has been received

# Repeat while there are more chunks to be received
while expectedLength > 0:

    # Try to receive the next 1024-byte chunk
    try:
        chunkFromServer, addr = s.recvfrom(1024)

    # If it times out, print an error and stop
    except socket.timeout:
        print("Failed to receive command output from server in time")
        sys.exit()

    # Else, process the chunk
    else:
        # Print chunk received
        print("Chunk of size ", len(chunkFromServer), " received")
        print(chunkFromServer)

        # Store its contents in a file
        f = open("client_udp_stdout.txt", "w")
        f.write( chunkFromServer.decode() )
        f.close()

        # Update the remaining expected length to be received
        expectedLength -= len(chunkFromServer)

# At this point, all expectedLength bytes have been received, so send an ACK

# Print sending ACK
print("Sending ACK to server")

# Send ACK back to server
s.sendto("ACK".encode(), serverAddr)