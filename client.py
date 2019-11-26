from socket import *
import pickle
import time
import sys
import threading
#data initialize
serverName = str(sys.argv[1])
serverPort = int(sys.argv[2])
auth = False
TIMEOUT_INTERVAL = 240
client_name = ''
#receive messages from the server
def receiveFunction():
    global TIMEOUT_INTERVAL
    global client_name
    global TCP_Socket
    global auth
    while True:
        receivedMessage = TCP_Socket.recv(2048)
        receivedMessage = receivedMessage.decode()
        print(receivedMessage)
        if  receivedMessage == "":
             TCP_Socket.close()
             return
        #to deal with block feedback
        if  ("you have been block.pls wait\
                                          20 sec to try again" == receivedMessage):
            TCP_Socket.close()
            exit()
        #to deal with welcome feedback
        if ('Welcome' in receivedMessage):
            print(receivedMessage)
            client_name = receivedMessage.split(' ')[1]
            auth = True
        #to deal with timeout feedback
        if ('timeout' in receivedMessage):
            return
        #to deal with whoelse feedback
        if ('whoelse' in receivedMessage):
            pass
        TCP_Socket.settimeout(TIMEOUT_INTERVAL)

# establish connection
TCP_Socket = socket(AF_INET, SOCK_STREAM)
TCP_Socket.connect((serverName, serverPort))
t1 = threading.Thread(target=receiveFunction)
t1.setDaemon(True)
t1.start()
while True:
    a = input()
    if  a == 'logout':
        logout_mes = client_name + " haslogout"
        client_name = ''
        TCP_Socket.send(logout_mes.encode())
        TCP_Socket.close()
    if a == 'whoelse':
        infor_whoelse = 'whoelse'
        TCP_Socket.send(infor_whoelse.encode())
    a = a.encode()
    TCP_Socket.send(a)
    
