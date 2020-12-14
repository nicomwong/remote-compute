## Introduction
You can use these programs to open a local TCP or UDP server and client.
The client sends a UNIX command to the server which then processes it locally and returns its output.
Both the client and server store the received/computed output in their respective text files.
By default, packets are sent in 8 bytes to demonstrate the Application-layer implemented stop & wait acknowledgement (ACK) protocol but this can be changed in the code.

## Client-Server Workflow
1. Client sends the command length and command to the server then waits for the output from the server.
    If the client does not hear back within 1 second, it ditches the message.
2. Server receives the command length and command, and then it validates that the length matches
3. If it matches, the server runs the command locally and stores its output in `server_udp_stdout.txt`
4. Server sends contents of this output text file back to the client in constant-sized packets and then waits for an ACK back from the client
5. Client receives a packet and sends an ACK to the server
6. Server receives ACK and moves on to the next packet.
    If the server does not receive an ACK in a certain timeframe, it resends the packet and waits for an ACK again.
    The same packet is resent a maximum of 3 times before it ditches the message.
7. 4, 5, and 6 repeat until all packets are sent from server to client
8. Finally, the client stores all of the combined packet data into `client_udp_stdout.txt`

## Supported commands
1. Any unix command stores the kernel output (stdout)
2. `cmd > fileName` stores the output of `cmd` into a file with name `fileName`

## Example

#### Terminal Window 1 in .../SocketProgramming/udp

`$ python server_python_udp.py 9999`
\
Server is now up!

#### Terminal Window 2 in .../SocketProgramming/udp

```
$ python client_python_udp.py
Enter server name or IP address: localhost
Enter port: 9999
Enter command: date
Sent command length and command to server
ACK received
Expected length is 29
Packet of size 8 received
b'Tue Dec '
Sending ACK
Packet of size 8 received
b' 1 01:02'
Sending ACK
Packet of size 8 received
b':03 PST '
Sending ACK
Packet of size 5 received
b'2020\n'
Sending ACK
File client_udp_stdout.txt saved
```

