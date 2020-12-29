import struct
import os
from myGetch import getch
from socket import *

LISTEN_PORT = 13117
Magic_cookie = 0xfeedbeef
group_name = "Pazim\n"

#Looking for a server
udp_socket = socket(AF_INET, SOCK_DGRAM) # UDP
udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
try:
    udp_socket.bind(('', LISTEN_PORT))
except:
    print('problem')

print('Client started, listening for offer requests...')

while True:
    data, addr = udp_socket.recvfrom(1024)
    unpack_data = struct.unpack('Ibh',data)
    temp_magic=unpack_data[0]
    temp_type=unpack_data[1]
    if (temp_magic == Magic_cookie and temp_type == 0x2):
        break

TCP_IP = addr[0]
TCP_PORT = unpack_data[2]

print('Received offer from ' +str(TCP_IP) +', attempting to connect...')


#initiate TCP socket
tcp_socket = socket(AF_INET, SOCK_STREAM)
server_address = (TCP_IP, TCP_PORT)

# Connecting to a server
while True:
    try:
        tcp_socket.connect(server_address)
        break
    except:
        pass

#send group name
tcp_socket.sendall(group_name.encode())

#Game mode
try:
    server_msg = tcp_socket.recv(1024)
except: 
    pass #error
server_msg=server_msg.decode()
print(server_msg)

server_msg = None
tcp_socket.setblocking(False)
while True:
    try:
        server_msg = tcp_socket.recv(1024)
        break   
    except:
        pass     
    c=getch()
    if c != None:
        tcp_socket.sendall(c)

server_msg = server_msg.decode()
print(server_msg)
print("Server disconnected, listening for offer requests...")
tcp_socket.close()

    


