import socket
import sys
import threading

class client:
    def __init__(self, username):
        self.username = username
    
    def connectToServer(self):
        serverAddress = ('localhost', 6667)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect(serverAddress)
        self.clientSocket.sendall(f"{self.username}".encode('utf-8'))
    
    def sendMessage(self):
        while True:
            message = input("Enter message: ")
            if(message.lower == "exit" or message.lower == "quit"):
                self.clientSocket.sendall(message.encode('utf-8'))
                break
            self.clientSocket.sendall(message.encode('utf-8'))
        self.clientSocket.close()

    def receiveMessage(self):
        while True:
            try:
                data = self.clientSocket.recv(1024)
                if data:
                    msg = data.decode('utf-8')
                    if msg == "Server is shutting down":
                        print("Server is shutting down. Ending connection")
                        self.clientSocket.close()
                        sys.exit(0)
                    print(f"Received: {msg}")
            except ConnectionResetError:
                break

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("Error: requires a username as an argument")
        exit(1)
    username = sys.argv[1]
    client = client(username)
    client.connectToServer()

    print(f"Connected to server with username: {username}")
    sendThread = threading.Thread(target=client.sendMessage)
    receiveThread = threading.Thread(target=client.receiveMessage)

    sendThread.start()
    receiveThread.start()
    sendThread.join()
    receiveThread.join()

    # while True: 
    #     message = input("Enter message: ")
    #     if(message.lower == "exit" or message.lower == "quit"):
    #         break
    #     client.sendMessage(clientSocket, message)
    #     client.receiveMessage(clientSocket)