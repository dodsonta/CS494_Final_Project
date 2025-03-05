import socket
import sys
import threading
import time

DEBUG = False

class client:
    def __init__(self, username):
        self.username = username
        self.online = True
    
    def connectToServer(self):
        serverAddress = ('localhost', 6667)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect(serverAddress)
        self.clientSocket.sendall(f"{self.username}".encode('utf-8'))
    
    def sendMessage(self):
        while self.online == True:
            message = input("Enter command:\n")
            if self.online == False:
                break
            if(message == "EXIT"):
                self.online = False
                print("Exiting client")
                self.clientSocket.sendall(message.encode('utf-8'))
                break
            self.clientSocket.sendall(message.encode('utf-8'))
            time.sleep(0.5)
        self.clientSocket.close()

    def receiveMessage(self):
        while self.online == True:
            try:
                data = self.clientSocket.recv(1024)
                if data:
                    msg = data.decode('utf-8')
                    if msg == "SHUTDOWN":
                        print("\nReceived: Server is shutting down. Ending connection")
                        self.online = False
                        self.clientSocket.close()
                        sys.exit(0)
                    elif msg.startswith("MESSAGE") or msg.startswith("LEFT") or msg.startswith("JOINED"):
                        msg = msg.split(" ", 1)[1]
                        print(f"\nReceived:\n{msg}\nEnter command: ")
                    else:
                        print(f"\nReceived:\n{msg}\n")
            except ConnectionResetError:
                break
            except OSError:
                break

if __name__ == "__main__":

    if DEBUG == True:
        print("Debug mode enabled")
        username = "test"
    elif(len(sys.argv) != 2):
        print("Error: requires a username as an argument")
        exit(1)
    else:
        username = sys.argv[1]
    client = client(username)
    client.connectToServer()

    print(f"Connected to server with username: {username}\n Type HELP for a list of commands")
    sendThread = threading.Thread(target=client.sendMessage)
    receiveThread = threading.Thread(target=client.receiveMessage)

    sendThread.start()
    receiveThread.start()
    sendThread.join()
    receiveThread.join()