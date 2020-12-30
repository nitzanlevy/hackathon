import struct
import os
import time
from myGetch import getch
from socket import *
# from scapy.arch import get_if_addr

def crash():
    tcp_socket.close()
    print("Server disconnected, listening for offer requests...")

# CLIENT_IP = get_if_addr('eth1') 
LISTEN_PORT = 13117
Magic_cookie = 0xfeedbeef
group_name = "TCPP\n"

print('Trying to Connect')
#Looking for a server
udp_socket = socket(AF_INET, SOCK_DGRAM,IPPROTO_UDP) # UDP
# udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
while True:
    try:
        #bind until success
        udp_socket.bind(('', LISTEN_PORT))
        break
    except:
        time.sleep(0.1)
        continue

print('Client started, listening for offer requests...')
while True:

    #get offer from server until the data correct
    while True:
        data, addr= None,None
        try:
            data, addr = udp_socket.recvfrom(1024)
            unpack_data = struct.unpack('Ibh',data)
            temp_magic=unpack_data[0]
            temp_type=unpack_data[1]
            if (temp_magic == Magic_cookie and temp_type == 0x2):
                break
        except:
            print('incorrect data')
            continue

    TCP_IP = addr[0]
    TCP_PORT = unpack_data[2]

    print('Received offer from ' +str(TCP_IP) +', attempting to connect...')


    #initiate TCP socket
    tcp_socket = socket(AF_INET, SOCK_STREAM)

    connected = False
    # Connecting to a server
    while True:
        try:
            tcp_socket.connect((TCP_IP, TCP_PORT))
            connected=True
            break
        except:
            break
    
    if not connected:
        crash()
        continue

    try:
        #send group name
        tcp_socket.sendall(group_name.encode())

        #Game mode
        server_msg = tcp_socket.recv(1024).decode()
        #print welcome message
        print(server_msg)

        server_msg = None
        tcp_socket.setblocking(False)
    except:
        crash()
        continue

    while True:
        try:
            server_msg = tcp_socket.recv(1024).decode()
            #print winners message
            print(server_msg)
            break   
        except:
            c=getch()
            if c != None:
                try:
                    tcp_socket.sendall(c)
                except:
                    break     
            
    crash()
    time.sleep(0.05)
    



    


    


