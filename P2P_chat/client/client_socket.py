from config import *
import socket
#same as the ServerSocket，used for Socket initialization
class ClientSocket(socket.socket):
    def __init__(self):
        #No need to bind port number or set listener mode
        super(ClientSocket,self).__init__(socket.AF_INET,socket.SOCK_STREAM)
        #self.sock=sock
        #self.bind((SERVER_IP,SERVER_PORT))
        #self.listen(128)
    def connect(self):
        ####here connect override，so it is called in the following mode
        #Call this function to connect the client to the server 
        # (where the server's address and port number are required）
        #in server.py, it allows the client to connect to the server via connect 
        #and get its socket and address via
        #soc, addr = self.server_socket.accept()
        #The server can obtain the socket of the client to perform various operations

        #connect the server
        super(ClientSocket,self).connect((SERVER_IP,SERVER_PORT))

    #write the send and receive data in socket.py
    def recv_data(self):
        try:
          return self.recv(512).decode('utf-8')
        except:
            return ''
    def send_data(self,message):
        return self.send(message.encode('utf-8'))
    def close(self):
        #print('duck')
       self.close()
if __name__== '__main__':
    t=ClientSocket()
    t.close()