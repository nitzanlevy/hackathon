import time
import random
from threading import Thread
import threading
import os
import struct
import sys
from socket import *
from _thread import *


HEADER = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[93m'
sys.stdout.write(HEADER)

threads = []   
in_game_mode = False
threadLock = threading.Lock()
TCP_PORT = 2013
UDP_PORT = 13117
LOCAL_IP = '192.168.1.43'
BUFFER_SIZE = 1024
TTL = 10
group1 = ''
group2 = ''
score1 = 0 
score2 = 0

# Create a UDP socket
udp_socket = socket(AF_INET, SOCK_DGRAM)
# Enable broadcasting mode
udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

# Create a TCP socket
tcp_socket = socket(AF_INET, SOCK_STREAM)
# Binding to local port 1033
tcp_socket.bind(('', TCP_PORT))
# Listen for incoming connections
tcp_socket.listen()


#handle connection per client
def funClient(tcp_socket): 
    global group1, group2, score1, score2, timer,threadLock,in_game_mode
    
    sys.stdout.write(GREEN)
    print('client connected')
    sys.stdout.write(HEADER)
    
    #put the client in group1 or group2, randomly
    try:
        client_name = tcp_socket.recv(BUFFER_SIZE).decode()
    except:
        tcp_socket.close()
        return
        
    rand = random.randint(1,2)
    if rand==1:
        group1 = group1 + (client_name)
    else:
        group2 = group2 + (client_name)

    #wait until 10 seconds pass since the server send requests
    while True:
        if timer==TTL:
            break
        time.sleep(0.1)

    #game start's message
    game_start_message = "Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n"+group1+"\nGroup 2:\n==\n"+group2+"\nStart pressing keys on your keyboard as fast as you can!!"
    in_game_mode = True
    try:
        tcp_socket.send(game_start_message.encode())
        tcp_socket.settimeout(0.1)
    except:
        in_game_mode = False
        tcp_socket.close()
        return

    #game mode
    start = time.time()
    while time.time()-start<TTL:
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

    #calculate the winners    
    if score1>score2 : 
        winners_msg = "Game over!\nGroup 1 typed in "+ str(score1)+" characters. Group 2 typed in "+ str(score2) +" characters.\nGroup 1 wins!\nCongratulations to the winners:\n==\n"+ group1
    else: 
        winners_msg = "Game over!\nGroup 1 typed in "+ str(score1)+" characters. Group 2 typed in "+ str(score2) +" characters.\nGroup 2 wins!\nCongratulations to the winners:\n==\n"+ group2
    try:
        tcp_socket.send(winners_msg.encode())
    except:
        pass
    
    #game over , close the connection with the client
    in_game_mode = False
    tcp_socket.close()


#thread for accepting new connections
def accept_socket ():
    while True:
        try:
            client_socket, address = tcp_socket.accept()
            t=Thread(None ,funClient,None, (client_socket, ))
            t.start()
            threads.append(t)
        except:
            continue



#start the server
start_new_thread(accept_socket,())

print('Server started, listening on IP address ' + LOCAL_IP)

while True:
    group1 = ''
    group2 = ''
    score1 = 0 
    score2 = 0
    timer = 0
    if not in_game_mode:

        #send requests
        message = struct.pack('Ibh', 0xfeedbeef, 0x2, TCP_PORT)
        timer = 0
        for i in range(TTL,0,-1):
            udp_socket.sendto(message, ('<broadcast>', UDP_PORT))
            print("waiting for a client...")
            time.sleep(1)
        timer = TTL

        #in game mode
        sys.stdout.write(BLUE)
        for i in range(TTL,0,-1):
            print('game over in', str(i), 'sec')
            time.sleep(1)

    #wait for all threads to finish    
    for t in threads:
        t.join()
    sys.stdout.write(GREEN)

    #game over, repeat
    print("Game over, sending out offer requests...")
    sys.stdout.write(HEADER)
