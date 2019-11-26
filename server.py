from socket import *
import pickle
import sys
import threading
import time
#user data processes
with open('credentials.txt') as f:
    user_data = f.readlines()
user_list = []
for i in user_data:
    i = i.replace('\n', '')
    user_list.append(i)
dic = {}
user_status = {}
user_socket = {}
onlie_dic = {}

for i in user_data:
    dic[i.split()[0]] = i.split()[1]
    user_status[i.split()[0]] = 2
    user_socket[i.split()[0]] = ''

block_list = []
online_list = []

#realize block function
def block_slp(name):
    global block_list
    time.sleep(20)
    block_list.remove(name)

#main function by the server
def comm(connectionSocket):
    global TIMEOUT_INTERVAL
    global online_list
    global allClients
    global user_status
    global user_socket
    global dic
    global block_list
    global onlie_dic
    allClients[currPort] = connectionSocket

    count = 0
    while True:

        count = 0
        connectionSocket.send("username:".encode())
        msg = connectionSocket.recv(2048).decode()

        if msg in block_list:
            connectionSocket.send("user has been blocked".encode())
            print(block_list)
            continue

        if msg not in dic:
            re = 'it is not valid user'.encode()
            connectionSocket.send(re)
            continue
        else:
            while True:
                print(dic[msg.strip()])
                if count == 3:
                    block_list.append(msg)
                    t2 = threading.Thread(target=block_slp, args=(msg,))
                    t2.setDaemon(True)
                    t2.start()

                    connectionSocket.send("you have been block.pls wait\
                                          20 sec to try again".encode())
                    return

                connectionSocket.send("password:".encode())
                msg1 = connectionSocket.recv(2048).decode()
                #login judgement
                if msg1 == dic[msg.strip()]:

                    print(msg.strip())
                    print(user_status[msg.strip()])
                    user_status[msg.strip()] = 1
                    wel = "Welcome " + str(msg.strip())
                    print(wel)
                    connectionSocket.send(wel.encode())

                    for i in list(onlie_dic):
                        mss = str(msg.strip()) + ' has logged in'
                        onlie_dic[i].send(mss.encode())
                    onlie_dic[msg.strip()] = connectionSocket

                    receive(connectionSocket)



                    return
                else:
                    count += 1
                    connectionSocket.send("password is wrong".encode())
                    continue



#the second main function by the server
def receive(connectionSocket):
    global onlie_dic
    while 1:
        msg = connectionSocket.recv(2048).decode()
        print(msg)

        if msg == '':
            connectionSocket.close()
            return

        #to deal with logout requests
        if 'logout' in msg:

            del onlie_dic[msg.split()[0]]
            for i in onlie_dic:
                # print(msg.split()[0]+" this is send logout client")
                i = str(i)
                mss = str(msg.split()[0]) + ' has logged out'
                onlie_dic[i].send(mss.encode())
        #to deal with whoelse requests
        if 'whoelse' in msg:
            if len(onlie_dic) == 1:
                mss = 'no one except youself'
                connectionSocket.send(mss.encode())

            for i in onlie_dic:
                # print(msg.split()[0]+" this is send logout client")
                i = str(i)
                mss = str(i) + ' whoelse'
                connectionSocket.send(mss.encode())
        #to deal with broadcast requests
        if 'broadcast' in msg:
            msg = msg.split()[1:]
            mss = ''
            for j in msg:
                print(j)
                mss += j
                print(mss)
            print("in broadcast function")
            for i in onlie_dic:

                if onlie_dic[i] == connectionSocket:

                    continue
                else:
                    pass
                    #print(" this is send logout client")





                    print("dic key is "+str(i))

                    onlie_dic[i].send(mss.encode())

                    print('have send')



    return


#data initialize
serverName = str(sys.argv[1])
serverPort = int(sys.argv[2])
    #input('client:')
currPort = 6001
auth = False
allClients = {}
TIMEOUT_INTERVAL = int(sys.argv[3])
    #input('timeout:')
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(0)
serverSocket.settimeout(TIMEOUT_INTERVAL)
# sys.exit()

while True:
    print('server is ready')
    connectionSocket, addr = serverSocket.accept()

    t1 = threading.Thread(target=comm, args=(connectionSocket,))
    t1.setDaemon(True)
    t1.start()

    print ("logout?")
    logg = input()
    if logg == 'out':
        break

    else:
        pass



connectionSocket.close()



