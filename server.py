import socket
import random
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_Address= "127.0.0.1"
port= 8000
server.bind((ip_Address, port))
server.listen()
clients = []
nicknames = []

def remove(connection):
    if connection in clients:
        clients.remove(connection) 
  
def broadcast(conn, msg):
    for client in clients:
        if client != conn:
            try:
                client.send(msg.encode("utf-8"))
            except:
                remove(client)

def clientThread(conn, nickname):
    conn.send("Welcome to the chatroom!".encode("utf-8"))
    while(True):
        try:
            msg = conn.recv(2048).decode("utf-8")
            if msg:
                    print(msg)
                    broadcast(conn, msg)
                    # conn.send(msg.encode("utf-8"))
            else:
                remove(conn)
        except:
            pass  
while(True):
    connection, address = server.accept()
    connection.send("NICKNAME".encode("utf-8"))
    nickname = connection.recv(2048).decode("utf-8")
    nicknames.append(nickname)
    print(nickname + " connected!")
    clients.append(connection)
    newThread = Thread(target=clientThread, args=(connection,nickname))
    newThread.start()
