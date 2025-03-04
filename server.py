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
                if message == "EXIT":
                    break
                elif message == "HELP":
                    self.clients[username].sendall("Commands:\n HELP: Display Commands \n \
EXIT: Exit the server\n \
SEARCH ROOMS: Search list of rooms\n \
CREATE ROOM <room name>: Creates a room of the name inputted into room name \n \
JOIN ROOM <room name>: Joins a room of the name inputted into room name \n \
LEAVE ROOM <room name>: Leaves a room of the name inputted into room name \n \
LIST USERS <room name>: Lists users in a room of the name inputted into room name \n \
[<room name>, ..] <message>: Sends a message to all users in the room of the name inputted into room name(s), can send to multiple rooms with commas seperating them. Note must keep brackets \n \
                                                   ".encode('utf-8'))
                elif message == "SEARCH ROOMS":
                    self.clients[username].sendall(f"Rooms: {self.rooms}".encode('utf-8'))
                elif message.startswith("CREATE ROOM "):
                    roomName = " ".join(message.split(" ")[2:])
                    self.rooms[roomName] = []
                    self.clients[username].sendall(f"Room {roomName} created".encode('utf-8'))
                elif message.startswith("JOIN ROOM "):
                    roomName = message.split(" ")[2]
                    if roomName in self.rooms:
                        self.rooms[roomName].append(username)
                        self.clients[username].sendall(f"Joined room {roomName}".encode('utf-8'))
                    else:
                        self.clients[username].sendall(f"Room {roomName} does not exist".encode('utf-8'))
                elif message.startswith("LEAVE ROOM "):
                    roomName = message.split(" ")[2]
                    if (roomName in self.rooms) and (username in self.rooms[roomName]):
                        self.rooms[roomName].remove(username)
                        self.clients[username].sendall(f"Left room {roomName}".encode('utf-8'))
                        for user in self.rooms[roomName]:
                            self.clients[user].sendall(f"{username} left room {roomName}".encode('utf-8'))
                    elif roomName in self.rooms:
                        self.clients[username].sendall(f"You are not in room {roomName}".encode('utf-8'))
                    else:
                        self.clients[username].sendall(f"Room {roomName} does not exist".encode('utf-8'))
                elif message.startswith("LIST USERS "):
                    roomName = message.split(" ")[2]
                    if roomName in self.rooms:
                        self.clients[username].sendall(f"Users in room {roomName}: {self.rooms[roomName]}".encode('utf-8'))
                    else:
                        self.clients[username].sendall(f"Room {roomName} does not exist".encode('utf-8'))
                elif message.startswith("["):
                    rooms = message.split("]")[0].split("[")[1].split(", ")
                    message = message.split("]")[1].strip()
                    for room in rooms:
                        if (room in self.rooms) and (username in self.rooms[room]):
                            for user in self.rooms[room]:
                                if user != username:
                                    self.clients[user].sendall(f"Room: {room}, User: {username}: {message}".encode('utf-8'))
                        elif room in self.rooms:
                            self.clients[username].sendall(f"You are not in room {room}".encode('utf-8'))
                        else:
                            self.clients[username].sendall(f"Room {room} does not exist".encode('utf-8'))
                else:
                    self.clients[username].sendall("Invalid command, type HELP to get a list of commands".encode('utf-8'))
            except socket.timeout:
                continue
            except ConnectionResetError:
                break
        if self.online:
            clientSocket.close()
            del self.clients[username]
            print(f"{username}  disconnected")

    def signal_handler(self, sig, frame):
        print("Exiting server")
        self.online = False
        time.sleep(2)
        for user in self.clients:
            try:
                self.clients[user].sendall("SHUTDOWN".encode('utf-8'))
                self.clients[user].close()
                print(f"{user} disconnected")
            except Exception as e:
                print(f"Error shutting down {user}: {e}")
        if self.serverSocket:
            self.serverSocket.close()
        sys.exit(0)

if __name__ == "__main__":
    server = Server()
    server.startServer()