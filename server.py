from socket import *

IP = '127.0.0.1'
PORT = 60000
BUFLEN = 1024

listen_socket = socket(AF_INET, SOCK_STREAM)

listen_socket.bind((IP, PORT))

listen_socket.listen(5)

print(f'Server: Service is running on port {PORT}. Waiting for client connection...')


data_socket , ip_port = listen_socket.accept()
print(f'Server >>> Accept a client {ip_port} connection')

while True:
    recved = data_socket.recv(BUFLEN)

    if not recved:
        print("Client close the connection.")
        break

    info = recved.decode('utf-8')

    print(f'Server >>> Received from client: \n {info}')

    data_socket.send(f'Server >>> Server{(IP, PORT)} received the info\n{info}'.encode('utf-8'))


data_socket.close()
listen_socket.close()