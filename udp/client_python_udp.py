# client_python_udp.py

# UCSB CS 176A Fall 2020 HW #1 Socket Programming
# Nicholas M Wong, PID: 3018439
# Syntax/libraries learned from geeksforgeeks.org, w3schools.com, docs.python.org

import socket
import sys

# Establish a socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # AF_INET for ipv4 address family, SOCK_DGRAM means UDP protocol

# Get user input for parameters
host = input("Enter sever name or IP address: ")
port = int(input("Enter port: "))
if not(0 <= port <= 65535):
    print("Invalid port number")
    
command = input("Enter command: ")

serverAddr = (host, port)
fileName = "client_udp_stdout.txt"

serverAddr = (host, port)

# Track the number of times this message was resent
sentCount = 0

# Repeat sending command length and command a maximum of 3 times
while (sentCount < 4):

    # Send the command length to the server
    s.sendto( str( len(command) ).encode(), serverAddr)

    # Send the command to the server
    s.sendto(command.encode(), serverAddr)

    # Print
    print("Sent command length and command to server")

    # Set socket timeout to 1 s
    s.settimeout(1)

    # Wait for an ACK to be received
    try:
        ack, addr = s.recvfrom(1024)
    # If it times out, resend length and command
    except socket.timeout:
        sentCount += 1
        continue
    # Else, check if ACK was received
    else:
        # If ACK was received, then print that and set ack to received
        if ack.decode() == "ACK":
            print("ACK received")
            break
        # Else, resend length and command
        else:
            sentCount += 1
            continue
            
# If timeoutCount reached 3, then print failure and terminate
if sentCount >= 4:
    print("Failed to send command. Terminating.")
    s.close()
    sys.exit()

# Set socket timeout to 1 second
s.settimeout(1)

# Wait to receive the expected message length from the server
data, addr = s.recvfrom(1024)
expectedLength = int( data.decode() )
print("Expected length is", expectedLength)

# Empty the file contents
f = open(fileName, "w")
f.write("")
f.close()

# Store currently received message length
currLength = 0

# Repeat while there are more packets to be received
while currLength < expectedLength:

    # Set socket timeout to 500 ms
    s.settimeout(0.5)
    
    # Try to receive the next 1024-byte packet
    try:
        packetFromServer, addr = s.recvfrom(8)
    # If it times out, print an error and stop
    except socket.timeout:
        print("Failed to receive command output from server")
        s.close()
        sys.exit()
    # Else, append the packet to the file
    else:
        # Print packet received
        print("Packet of size", len(packetFromServer), "received")
        print(packetFromServer)

        # Append this packet's contents to the file
        f = open(fileName, "a")
        f.write( packetFromServer.decode() )
        f.close()

        # Send an ACK to the server that this packet was received
        print("Sending ACK")
        s.sendto("ACK".encode(), addr)

        # Update the currently received length
        currLength += len(packetFromServer)

# Check if the total received message length is as expected
if not(currLength == expectedLength):
    print("Failed to receive command output from server.")
    print("Expected", expectedLength, "bytes. Received", currLength, "bytes")
    s.close()
    sys.exit()

# At this point, all packets should have been received and stored, so print success
print("File", fileName, "saved")
s.close()