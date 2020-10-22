# server_python_udp.py

# UCSB CS 176A Fall 2020 HW #1 Socket Programming
# Nicholas M Wong, PID: 3018439
# Syntax/libraries learned from geeksforgeeks.org, w3schools.com, docs.python.org

import socket
import sys
import subprocess

def messageToPackets(message, packetSize):
    packetList = []

    messageSize = len(message)  # Remaining message size to be partitioned
    while messageSize > 0:
        beg = len(message) - messageSize
        end = beg + packetSize  # Note: end could be larger than len(message); python handles this
        packet = message[beg : end]
        packetList.append(packet)
        messageSize -= packetSize   # Update remaining message size
    
    return packetList

# Check for valid cmd line input
if ( len(sys.argv) != 2):
    print("Usage: python server_python_udp.py <port>")
    sys.exit()

# Set the port
port = int(sys.argv[1])
if not(0 <= port <= 65535):
    print("Invalid port number")

# Create a IPv4/UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to this machine with the port
s.bind( ('', port) )

# FOR TESTING: forced filename to save
fileName = "server_udp_stdout.txt"

# Infinite loop to wait for client connection
while True:

    # Set socket to blocking
    s.setblocking(True)
    
    # Wait to receive a command length from client
    cmdLength, addr = s.recvfrom(1024)

    # Set socket timeout to 500 ms
    s.settimeout(0.5)

    # Wait to receive command from client
    try:
        cmdFromClient, addr = s.recvfrom(1024)
    # If it times out, print an error and ditch the message
    except socket.timeout:
        print("Failed to receive instructions from the client.")
        continue
    # Else,
    else:
        # If the command is of the correct length, then respond with an ACK
        if len(cmdFromClient) == int( cmdLength.decode() ):
            print("Sending ACK")
            s.sendto("ACK".encode(), addr)
        # Else, print an error and ditch the message
        else:
            print("Failed to receive instructions from the client.")
            continue

    # Run the command on the shell from server and store the output
    stdout = subprocess.check_output( cmdFromClient.decode(), shell=True )

    # Put the output into a file
    f = open(fileName, "w")
    f.write( stdout.decode() )
    f.close()

    # Send the full message length to the client
    s.sendto(str( len(stdout) ).encode(), addr)

    # Track the number of times the message has been sent
    timesSent = 0

    # Partition the message into packets of size 1024
    packetList = messageToPackets(stdout, 1024)

    # Repeat for each packet to send
    for packet in packetList:

        # Repeat sending packet length and message a maximum of 3 times
        while timesSent < 3:

            # Send the packet to the client
            s.sendto(stdout, addr)

            # Set timeout to 1 second for ACK to be received
            s.settimeout(1)

            # Print
            print("Sent packet length and packet to client")
            
            # Wait for ACK to be received
            try:
                ack, addr = s.recvfrom(1024)
            # If it takes more than 1 second, resend message and length
            except socket.timeout:
                timesSent += 1
                continue
            # Else, check that the data was ACK
            else:
                # If it was ACK, print ACK received and continue to next packet
                if ack.decode() == "ACK":
                    print("ACK received")
                    break
                # Else, resend message and length
                else:
                    timesSent += 1
                    continue
        
        # If timesSent reached 3, print error and ditch this message
        if timesSent >= 3:
            print("File transmission failed.")
            continue