from socket import *
import threading

IP = '127.0.0.1'
PORT = 60000
BUFLEN = 1024

listen_socket = socket(AF_INET, SOCK_STREAM)

listen_socket.bind((IP, PORT))

listen_socket.listen(5)

print(f'[Server] Service is listenning on port {PORT}. Waiting for client connection...')


data_socket , ip_port = listen_socket.accept()
print(f'[Server] Accept a client {ip_port} connection.')

def listen_disp():
    while True:
    	recved = data_socket.recv(BUFLEN)

    	if not recved:
        	print("Client close the connection and I close too.")
        	break
    	info = recved.decode('utf-8')

    	print(f'<Client> {info}')

thr1 = threading.Thread(listen_disp())

while True:
    thr1.start()
    toSend = input('Server >>')
    if toSend == 'exit':
        break

    data_socket.send(toSend.encode('utf-8'))

    recved = data_socket.recv(BUFLEN)

    if not recved:
        break

    print(recved.decode('utf-8'))
    # data_socket.send(f'[Server] Server{(IP, PORT)} received the info\n{info}'.encode('utf-8'))

data_socket.close()
listen_socket.close()