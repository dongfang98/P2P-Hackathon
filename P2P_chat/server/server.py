from serversocket import ServerSocket
from socket_wrapper import SocketWrapper
from threading import Thread
from config import *
from responseprotocol import *
from db import DB
class Server(object):
    def __init__ (self):
        ####start the server
        self.server_socket=ServerSocket()
        #create a dictionary to get a id

        self.request_handle_function = {}
        #Each key point to a function, so that it will be easier to call different function

        self.request_handle_function[REQUEST_LOGIN] = self.request_login_handle
        self.request_handle_function[REQUEST_CHAT] = self.request_chat_handle
    
        #save the data of client witch successfully login 
        self.clients={}

        #database part
        self.db=DB()

    def startup(self):
        while True:
            print('obtaining links from client')
            #client can connect to the server and get the address and socket

            soc,addr=self.server_socket.accept()
            print('link obtained')
            #Wrapper the socket

            client_soc=SocketWrapper(soc)
            #Use multprocessing to handle multiple client to access to the server

            t=Thread(target=self.request_handle,args=(client_soc,))
            t.start()
            #self.request_handle(client_soc)

    def request_handle(self,client_soc):
        print('handling request')
        #handle the request of client

        while True: 
            #receive the data from client

            recv_data = client_soc.recv_data()
            if not recv_data:
                #In this case, the client will keep sending messages to the server, when the client disconnect, server can not 
                #any message from server, so we can judge wether the client is offline and remove the data of client

                self.remove_offline_user(client_soc)
                client_soc.close()
                break
            #Parse the data, get information about the type of request
        
            parse_data=self.parse_request_text(recv_data)
            #From request_id, we can know the whether the request is login or chat, and call corresponding function

            handle_function =self.request_handle_function.get(parse_data['request_id'])
            #call the function

            if handle_function:
                handle_function(client_soc,parse_data)
            #same function with previous code
            #if pares_data['request_id'] == REQUEST_LOGIN:
                #self.request_login_handle()
            #elif parse_data['request_id'] == REQUEST_CHAT:
                #self.request_chat_handle()

    def request_login_handle(self,client_soc,request_data):
        print('login handle')
        #This part will handle the login request
：
        #Get username and password
        username = request_data['username']
        password = request_data['password']

        #check whether the data match database

        ret,nickname,username=self.check_user_login(username,password)
        if ret =='1':
            self.clients[username]={'sock':client_soc,'nickname':nickname}
            print('login success')
            #clients is a dictionary to save the data of successfully login client's socket
            #The key is its username and value is another dictionary which save the socket and nickname


        #if login successfully, the server will save its data, and return 1001|1|nickname|username to client, if failed, 
        #return  1001|0| | ,the username and nickname is None

        response_text=ResponseProtocol.response_login_result(ret,nickname,username)
        client_soc.send_data(response_text)

    def check_user_login(self,username,password):
        #Check whether the cilent login successfully, 1 means success

        print('checking user login',username)
        #Data from in db： user_id | user_name | user_password | user_nickname

        sql="select * from users WHERE user_name='%s'" % username
        result= self.db.get_one(sql)

        #Match the information with db, check if the user has register

        if not result:
            return '0','',username
        #match the password
        #@@@
        else:
         if password != result['user_password']:
             return '0', '', username
         else:
           return'1',result['user_nickname'],username



    def request_chat_handle(self,client_soc,request_data):
        #forward messages to all client online
        #parse_data is wrapped dictionary which contain information of client 

        #Get username, message nickname, password

        username=request_data['username']
        messages=request_data['messages']
        nickname=self.clients[username]['nickname']

        #Join message together
        #if user do not login, nickname will be None
        msg=ResponseProtocol.response_chat(nickname,messages)

        #Send message to all user except myself

        if username in self.clients:

          for Username,info in self.clients.items():

              #clinet1 -> server -> all client, the message need to be parsed
              #clinet1 dose not have to wait server send message back

              if username != Username:
                  #continue
                info['sock'].send_data(msg)

    def remove_offline_user(self,client_soc):
        #clients is a dictionary to save successfully login user
        #key is its username
        #value is another dictionary to save socket and nickname
        # self.clients[username]={'sock':client_soc,'nickname':nickname}
        #.items is a function to traverse key and value in dictionary
        #username is the key of 'clients' and the info is the value of 'client'
        for username, info in self.clients.items():
            #find offline user and remove it forn dictionary

            if info['sock'] == client_soc:
                del self.clients[username]
                break
    def parse_request_text(self,recv_data):
        #parse data and form
        #clinet send to server:
        #login: 0001|username|password
        #chat:  0002|username|messages

        #server to client:
        #response of login：1001|ret|nickname|username
        #if login failed, username and nickname is None

        #split each part and save it in dictionary
        request_list=recv_data.split(DELIMITER)
        request_data={}
        request_data['request_id']=request_list[0]
        if request_data['request_id'] == REQUEST_LOGIN:
            request_data['username']= request_list[1]
            request_data['password']= request_list[2]
        elif request_data['request_id']== REQUEST_CHAT:
            request_data['username'] = request_list[1]
            request_data['messages'] = request_list[2]
        return(request_data)



if __name__ == '__main__':
    Server().startup()




#drop database mini_chat