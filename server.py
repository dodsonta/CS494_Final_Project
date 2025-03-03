import socket
import threading
import sys
import signal
import time 

clients = {}
rooms = {}

class Server:
    def __init__(self, host='localhost', port=6667):
        self.serverAddr = (host, port)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.settimeout(1)
        self.clients = {}
        self.rooms = {}
        self.online = True

    def startServer(self):
        self.serverSocket.bind(self.serverAddr)
        self.serverSocket.listen(5)
        serverAddr = ('localhost', 6667)
        print("Server started and listening on port 6667")
        signal.signal(signal.SIGINT, self.signal_handler)
        while self.online:
            try:
                clientSocket, clientAddr = self.serverSocket.accept()
                clientThread = threading.Thread(target=self.handleClient, args=(clientSocket, clientAddr))
                clientThread.start()
            except socket.timeout:
                continue

    def handleClient(self, clientSocket, clientAddress):
        username = clientSocket.recv(1024).decode('utf-8')
        self.clients[username] = clientSocket
        print(f"Connected with user named: {username}")
        clientSocket.settimeout(1)
        while self.online:
            try:
                message = clientSocket.recv(1024).decode('utf-8')
                print(f"Received message from {username}: {message}")
                if(message.lower() == "exit" or message.lower() == "quit"):
                    break
                for user in self.clients:
                    if user != username:
                        self.clients[user].sendall(f"{username}: {message}".encode('utf-8'))
            except socket.timeout:
                continue
            except ConnectionResetError:
                break 
        clientSocket.close()
        del self.clients[username]
        print(f"{username}  disconnected")

    def signal_handler(self, sig, frame):
        print("Exiting server")
        self.online = False
        time.sleep(5)
        for user in self.clients:
            self.clients[user].sendall("Server is shutting down".encode('utf-8'))
            self.clients[user].close()
        if self.serverSocket:
            self.serverSocket.close()
        sys.exit(0)

if __name__ == "__main__":
    server = Server()
    server.startServer()