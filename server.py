import socket
import threading

clients = {}
rooms = {}

def handleClient(clientSocket, clientAddress):
    username = clientSocket.recv(1024).decode('utf-8')
    clients[username] = clientSocket
    print(f"Connected with user named: {username}")
    while True:
        message = clientSocket.recv(1024).decode('utf-8')
        print(f"Received message from {username}: {message}")
        if(message.lower() == "exit" or message.lower() == "quit"):
            break
        for user in clients:
            if user != username:
                clients[user].sendall(f"{username}: {message}".encode('utf-8'))

def startServer():
    serverAddr = ('localhost', 6667)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(serverAddr)
    serverSocket.listen(5)
    print("Server started and listening on port 6667")
    while True:
        clientSocket, clientAddr = serverSocket.accept()
        clientThread = threading.Thread(target=handleClient, args=(clientSocket, clientAddr))
        clientThread.start()

if __name__ == "__main__":
    startServer()