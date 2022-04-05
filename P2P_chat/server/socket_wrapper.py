class SocketWrapper(object):
    #This part is to decode and encode the message between server and client
    def __init__(self,sock):
        self.sock=sock
    def recv_data(self):
        #the client may use recv function after logoff, we use except to avoid error

        try:
           return self.sock.recv(512).decode('utf-8')
        except:
           return ''
    def send_data(self,message):
        return self.sock.send(message.encode('utf-8'))
    def close(self):
        self.sock.close()
        #print('duck')
