import time
import random
import threading
import os
import struct
from socket import *
from _thread import *

threadLock = threading.Lock()
TCP_PORT = 1033
UDP_PORT = 13117
LOCAL_IP = '192.168.1.43'
# SO_REUSEPORT = SO_REUSEADDR
# udp_socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)

# Create a UDP socket
udp_socket = socket(AF_INET, SOCK_DGRAM)
# Enable broadcasting mode
udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)


# Create a TCP/IP socket
tcp_socket = socket(AF_INET, SOCK_STREAM)
# Binding to local port 1033
tcp_socket.bind(('', TCP_PORT))
# Listen for incoming connections
tcp_socket.listen()


group1 = ''
group2 = ''
score1 = 0 
score2 = 0
def funClient(tcp_socket): 
    global group1, group2, score1, score2, timer,threadLock
    print('client connected')
    client_name = tcp_socket.recv(1024).decode()
    rand = random.randint(1,2)
    if rand==1:
        group1 = group1 + (client_name)
    else:
        group2 = group2 + (client_name)

    while True:
        if timer==10:
            break
    game_start_message = "Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n"+group1+"\nGroup 2:\n==\n"+group2+"\nStart pressing keys on your keyboard as fast as you can!!"
    tcp_socket.send(game_start_message.encode())

    start = time.time()
    tcp_socket.settimeout(0.1)
    while time.time()-start<10:
        try:
            key = tcp_socket.recv(1)
            if key:
                with threadLock:
                    if rand==1:
                        score1 += 1
                    else:
                        score2 += 1
        except:
            continue
        

    if score1>score2 : 
        winners_msg = "Game over!\nGroup 1 typed in "+ str(score1)+" characters.\nGroup 2 typed in "+ str(score2) +" characters.\nGroup 1 wins!\nCongratulations to the winners:\n==\n"+ group1
    else: 
        winners_msg = "Game over!\nGroup 1 typed in "+ str(score1)+" characters.\nGroup 2 typed in "+ str(score2) +" characters.\nGroup 2 wins!\nCongratulations to the winners:\n==\n"+ group2
    tcp_socket.send(winners_msg.encode())
    tcp_socket.close()

def accept_socket ():
    while True:
        try:
            client_socket, address = tcp_socket.accept()
            start_new_thread(funClient, (client_socket, ))
        except:
            continue

#start the server
start_new_thread(accept_socket,())

print('Server started, listening on IP address ' + LOCAL_IP)

message = struct.pack('Ibh', 0xfeedbeef, 0x2, TCP_PORT)
timer = 0
for i in range(10,0,-1):
    udp_socket.sendto(message, ('<broadcast>', UDP_PORT))
    print("waiting for a client...")
    time.sleep(1)
timer = 10

while True : 
    time.sleep(1)