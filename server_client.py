from socket import *
import threading
import asyncio
import typing
import threading
import time

LOCALHOST = '127.0.0.1'
PORT = 60000
BUFLEN = 1024

def send(send_socket: socket, to_name: str):
    while(True):
        send_msg = input()
        if send_msg == 'exit':
            break
        send_socket.send(send_msg.encode('utf-8'))
        # print(f"[Send] Send \"{send_msg}\" to {to_name}.")
    send_socket.close()

def recv(recv_socket: socket, from_name: str):
    while(True):
        recv_msg = recv_socket.recv(BUFLEN)
        if not recv_msg:
            break
        print(" "*15,"<"+from_name.capitalize()+">", recv_msg.decode('utf-8'))
    recv_socket.close()

def run_server(ip=LOCALHOST, port=PORT):
	listen_socket = socket(AF_INET, SOCK_STREAM)
	listen_socket.bind((ip, port))
	listen_socket.listen(2)
	print(f"[Listen] {ip} is waiting for connection on PORT {port}...")
	send_socket, (send_IP, send_PORT) = listen_socket.accept()
	# print(f"Accept a client from {target_IP} on PORT {target_PORT}.")
	# print(f"[Receive Socket] {IP} is waiting for connection on PORT {PORT}...")
	recv_socket, (recv_IP, recv_PORT) = listen_socket.accept()
	# print(f"Accept a client from {target_IP} on PORT {target_PORT}.")

	print("-"*30,"Connected", "-"*30)
	
	thr1 = threading.Thread(target=send, args=(send_socket, 'client'))
	thr2 = threading.Thread(target=recv, args=(recv_socket, 'client'))

	thr1.start()
	thr2.start()

	while True:
		if not thr1.is_alive() and not thr2.is_alive():
			break

	listen_socket.close()
	send_socket.close()
	recv_socket.close()
	print("-"*30, "Disconnected", "-"*30)

def run_client(ip=LOCALHOST, port = PORT):
	recv_socket = socket(AF_INET, SOCK_STREAM)
	send_socket = socket(AF_INET, SOCK_STREAM)
	time_wait = 0
	time_count = 1
	time_out = 100

	while True:
		try:
			recv_socket.connect((ip, port))
			send_socket.connect((ip, port))
			break
		except ConnectionRefusedError as e:
			if time_wait <= time_out:
				print(f"Connection Refused. Trying to connect after {time_count} seconds...")
				time_wait = time_wait+time_count
				time.sleep(time_count)
				time_count = 2 * time_count
			else:
				raise TimeoutError(f"Time out {time_out}")

	# print("Connect to recv socket!")
	# print("Connect to send socket!")

	print(f"Connecting to {(ip, port)}...")
	print("-"*30, "Connected", "-"*30)

	thr1 = threading.Thread(target=send, args=(send_socket, 'server'))
	thr2 = threading.Thread(target=recv, args=(recv_socket, 'server'))

	thr1.start()
	thr2.start()

	while True:
		if not thr1.is_alive() and not thr2.is_alive():
			break
	send_socket.close()
	recv_socket.close()
	print("-"*30, "Disconnected", "-"*30)