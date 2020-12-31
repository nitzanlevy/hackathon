import struct
import os
import time
from myGetch import getch
from socket import *
import sys

HEADER = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[93m'

LISTEN_PORT = 13117
Magic_cookie = 0xfeedbeef
group_name = "TCPP\n"
BUFFER_SIZE = 1024

sys.stdout.write(HEADER)

#handle any case of disconnection with server
def crash():
    tcp_socket.close()
    sys.stdout.write(RED)
    print("Server disconnected, listening for offer requests...")
    sys.stdout.write(HEADER)


#Looking for a server
udp_socket = socket(AF_INET, SOCK_DGRAM) # UDP
udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
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
            data, addr = udp_socket.recvfrom(BUFFER_SIZE)
            unpack_data = struct.unpack('Ibh',data)
            temp_magic=unpack_data[0]
            temp_type=unpack_data[1]
            if (temp_magic == Magic_cookie and temp_type == 0x2):
                break
        except:
            sys.stdout.write(RED)
            print('incorrect data')
            sys.stdout.write(HEADER)
            time.sleep(0.1)
            continue

    TCP_IP = addr[0]
    TCP_PORT = unpack_data[2]

    print('Received offer from ' +str(TCP_IP) +', attempting to connect...')


    #initiate TCP socket
    tcp_socket = socket(AF_INET, SOCK_STREAM)

    # Connecting to a server
    try:
        tcp_socket.connect((TCP_IP, TCP_PORT))
    except:
        continue
    
    try:
        #send group name
        tcp_socket.sendall(group_name.encode())

        #Game mode
        server_msg = tcp_socket.recv(BUFFER_SIZE)
        if (not server_msg  or len(server_msg)==0):
            crash()
            continue
        server_msg=server_msg.decode()
        #print welcome message
        sys.stdout.write(BLUE)
        print(server_msg)
        sys.stdout.write(HEADER)

        server_msg = None
        tcp_socket.setblocking(False)
    except:
        crash()
        continue

    while True:
        try:
            server_msg = tcp_socket.recv(BUFFER_SIZE)
            if (not server_msg  or len(server_msg)==0):
                crash()
                continue
            server_msg=server_msg.decode()
            #print winners message
            sys.stdout.write(GREEN)
            print(server_msg)
            sys.stdout.write(HEADER)       
            break   
        except:
            time.sleep(0.01)
            pass   
        c=getch()
        if c != None:
            try:
                tcp_socket.sendall(c)
            except:
                break      
    crash()
    time.sleep(0.05)
    



    


    


