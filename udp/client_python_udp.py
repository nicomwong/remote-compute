# client_python_udp.py

# UCSB CS 176A Fall 2020 HW #1 Socket Programming
# Nicholas M Wong, PID: 3018439
# Syntax/libraries learned from geeksforgeeks.org, w3schools.com, docs.python.org

import socket
import sys

# Establish a socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # AF_INET for ipv4 address family, SOCK_DGRAM means UDP protocol
s.settimeout(0.5)   # Set socket timeout to 500 ms

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

# Send the command to the server
s.sendto(command.encode(), serverAddr)

# Try to receive the message length
try:
    # Receive the expected message length from the server
    data, addr = s.recvfrom(1024)

# If it times out, print an error and stop
except socket.timeout:
    print("Did not receive length response in time")
    sys.exit()
else:
    expectedLength = int( data.decode() )

# At this point, the length message has been received

# Repeat while there are more chunks to be received
while expectedLength > 0:

    # Try to receive the next chunk
    try:
        chunk, addr = s.recvfrom(1024)

    # If it times out, print an error and stop
    except socket.timeout:
        print("Failed to receive data response from server in time")
        sys.exit()

    # Else, process the chunk
    else:
        # Print chunk received
        print("Chunk of size ", len(chunk), " received")
        print(chunk)

        # # Store its contents in a file
        # f = open("client_udp_stdout.txt", "w")
        # f.write( dataFromServer.decode() )
        # f.close()

        # Update the remaining expected length to be received
        expectedLength -= len(chunk)

# At this point, all expectedLength bytes have been received, so send an ACK

# Print sending ACK
print("Sending ACK to server")

# Send ACK back to server
s.sendto("ACK".encode(), serverAddr)