import socket
import sys

class client:
    def __init__(self, username):
        self.username = username
    
    def connectToServer(username):
        serverAddress = ('localhost', 5000)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(serverAddress)
        clientSocket.sendall(f"Hello from user {username}".encode('utf-8'))
        return clientSocket
    
    def sendMessage(clientSocket, message):
        clientSocket.sendall(message.encode('utf-8'))

    def receiveMessage(clientSocket):
        while True:
            data = clientSocket.recv(1024)
            print(f"Received: {data.decode('utf-8')}")

    

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        exit(1)
    username = sys.argv[1]
    clientSocket = client.connectToServer(username)

    print(f"Connected to server with username: {username}")

    while True: 
        message = input("Enter message: ")
        if(message.lower == "exit" or message.lower == "quit"):
            break
        client.sendMessage(clientSocket, message)
        client.receiveMessage(clientSocket)

    clientSocket.close()