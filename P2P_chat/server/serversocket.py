from config import *
import socket
class ServerSocket(socket.socket):
    def __init__(self):
        #initialize the mode: TCP
        #bind the prot and host
        #set listening mode

        super(ServerSocket,self).__init__(socket.AF_INET,socket.SOCK_STREAM)
        self.bind((SERVER_IP,SERVER_PORT))
        self.listen(128)
