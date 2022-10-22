from distutils.filelist import glob_to_re
from guietta import Gui, _, III, ___, R0
from PyQt5 import QtWidgets, QtCore
from server_client import *
import threading

IS_CONNECT = False
server_sockets = []

def send(gui : Gui, send_socket: socket, to_name: str):
    send_msg = gui.sendmsg

    if send_msg == 'exit':
        IS_CONNECT = False
        send_socket.close()
    else:
        gui.sendmsg = ""
        def func():
            gui.widgets['pte'].appendPlainText(send_msg)
        gui.execute_in_main_thread(func)
        send_socket.send(send_msg.encode('utf-8'))

def recv(gui : Gui, recv_socket: socket, from_name: str):
    while(True):
        recv_msg = recv_socket.recv(BUFLEN)
        if not recv_msg:
            break
        def func():
            gui.widgets['pte'].appendPlainText(
                " "*30+"<"+from_name.capitalize()+">"+recv_msg.decode('utf-8')
            )
        gui.execute_in_main_thread(func)
    recv_socket.close()


def run_server(gui : Gui, ip=LOCALHOST, port=PORT):
    listen_socket = socket(AF_INET, SOCK_STREAM)
    listen_socket.bind((ip, port))
    listen_socket.listen(2)
    def func():
        gui.status = "Listening..."
    gui.execute_in_main_thread(func)
    send_socket, (send_IP, send_PORT) = listen_socket.accept()
    recv_socket, (recv_IP, recv_PORT) = listen_socket.accept()

    def func():
        gui.status = "Connected"
    gui.execute_in_main_thread(func)
    
    server_sockets.append(send_socket)
    IS_CONNECT = True

    recv(gui, recv_socket, 'client') # 阻塞


    def func():
        gui.status = "DisConnected"
    gui.execute_in_main_thread(func)
    listen_socket.close()
    send_socket.close()
    recv_socket.close()
    IS_CONNECT=False
    server_sockets.pop()

def run_client(gui : Gui, ip=LOCALHOST, port=PORT):
    recv_socket = socket(AF_INET, SOCK_STREAM)
    send_socket = socket(AF_INET, SOCK_STREAM)
    time_wait = 0
    time_count = 1
    time_out = 100

    while True:
        try:
            def func():
                gui.status = "Connecting..."
            gui.execute_in_main_thread(func)
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

    def func():
        gui.status = "Connected"
    gui.execute_in_main_thread(func)

    server_sockets.append(send_socket)
    IS_CONNECT = True

    recv(gui, recv_socket, 'server') # 阻塞

    def func():
        gui.status = "DisConnected"
    gui.execute_in_main_thread(func)
    send_socket.close()
    recv_socket.close()
    IS_CONNECT=False
    server_sockets.pop()

def click_connect(gui : Gui, *args):
    if gui.server_select.isChecked() or gui.client_select.isChecked():
        if gui.server_select.isChecked():
            gui.execute_in_background(run_server, (gui, gui.ip, int(gui.port)))
        else:
            gui.execute_in_background(run_client, (gui, gui.ip, int(gui.port)))

def click_send(gui : Gui, *args):
    if gui.sendmsg != "" and gui.status == "Connected":
        gui.execute_in_background(send, (gui, server_sockets[0], 'client'))

pte = QtWidgets.QPlainTextEdit()
pte.setFocusPolicy(QtCore.Qt.NoFocus)
gui = Gui(
    [ 'IP'         , '__ip__'    ,___          ,  'PORT ' ,___       , '__port__'    , ['Connect']    ],
    ["Mode"        , (R0("server"),"server_select"), (R0("client"), "client_select"),___       ,___       ,  ("Status")     , ("status")  ],
    [(pte, "pte")  , ___         , ___         , ___      ,___       ,___            ,___             ],
    ['__sendmsg__' ,___          , ___         , ___      ,___       ,['Send']       ,___             ]
)
gui.Send = click_send
gui.Connect = click_connect
gui.status = "Disconnected"
gui.run()