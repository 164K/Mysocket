from socket import *

IP = '127.0.0.1'
PORT = 60000
BUFLEN = 1024

data_socket = socket(AF_INET, SOCK_STREAM)

data_socket.connect((IP, PORT))

while True:
    toSend = input('Client >>')
    if toSend == 'exit':
        break

    data_socket.send(toSend.encode('utf-8'))

    recved = data_socket.recv(BUFLEN)

    if not recved:
        break

    print(recved.decode('utf-8'))

data_socket.close()