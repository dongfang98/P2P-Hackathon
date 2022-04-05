from window_login import WindowLogin
from request_protocol import RequestProtocol
from config import *
from client_socket import ClientSocket
from threading import Thread
from tkinter.messagebox import showinfo
from window_chat import WindowChat
import sys
class Client(object):
    def __init__(self):
        #create a window for login
        
        self.window =WindowLogin()
        self.window.on_reset_button_click(self.clear_inputs)
        self.window.on_login_button_click(self.send_login_data)
        #self.window.on_window_close(self.exit)
        

        #create window for chat
        self.window_chat=WindowChat()
        #self.window_chat.on_window_close(self.exit)

        #hide chat window
        self.window_chat.withdraw()

        ###create socket for client
        self.conn=ClientSocket()

        self.response_handle_function={}
        self.response_handle_function[RESPONSE_LOGIN_RESULT]=self.response_login_handle
        self.response_handle_function[RESPONSE_CHAT]=self.response_chat_handle
        self.window_chat.on_send_button_click(self.send_chat_data)

        #define a global variable to recode username online
        self.username=None

        #Whether the program is running
        self.isrunning= True
    def startup(self):
        
        #connect client socket to the server

        self.conn.connect()

        #Client may receive message at anytime, so we put this process in a thread
        #in the server, we use a loop in start up function to wait for the response of client
        #every loop we create a sub thread to check whether there is new client request
        #In client we just need to start once, beacuse mainloop is an endless loop
        #Then we start response_handle, and loop in sub thread 

        t=Thread(target=self.response_handle)
        t.start()

        #start login window is a endless loop, we put this at the last of the program
        self.window.mainloop()

    def clear_inputs(self):
        #clear window
        self.window.clear_username()
        self.window.clear_password()
    def send_login_data(self):

        #send request, username and password to server
        #get username and password input

        username=self.window.get_username()
        password=self.window.get_password()
 
        #create a protocol and wrappe it
        request_text = RequestProtocol.request_login_result(username,password)

        #send it to server
        self.conn.send_data(request_text)


    def response_handle(self):

        #continually accept data from server
        #while self.isrunning:
        while True:
          recv_data=self.conn.recv_data()

          #parse data(dictionary)
          response_data=self.parse_response_data(recv_data)

          #according to message processing,handle the data
          handle_function=self.response_handle_function.get(response_data['response_id'])
          if handle_function:
             handle_function(response_data)

          #if response_data['response_id']==RESPONSE_LOGIN_RESULT:
              #self.response_login_handle(response_data)
          #elif response_data['response_id']==RESPONSE_CHAT:
              #self.response_chat_handle(response_data)
    #self is not used in a static function
    @staticmethod
    def parse_response_data(recv_data):

        #There are two ways to handle messafe
        #1. server send a login request 1001|success|nickname|username or 1001|fail| 
        #2. server send a chat request 1002|nickname|message

        response_data_list=recv_data.split(DELIMITER)
        ####
        response_data={}
        response_data['response_id']=response_data_list[0]

        if response_data['response_id']==RESPONSE_LOGIN_RESULT:
            response_data['result']=response_data_list[1]
            response_data['nickname']=response_data_list[2]
            response_data['username']=response_data_list[3]

        elif response_data['response_id']==RESPONSE_CHAT:
            response_data['nickname']=response_data_list[1]
            response_data['message']=response_data_list[2]
        return response_data
    def response_login_handle(self,response_data):
        #response login
        print('Login result recieved')
        result = response_data['result']
        if result == '0':
            print('Login Failed')

            #print the title and content
            showinfo('Login result','Login Failed,wrong information!')
            return

        showinfo('Login result','Login Success!')
        nickname=response_data['nickname']
        self.username=response_data['username']
        print('%s has successfully login,nickname is %s'%(self.username,nickname))

        #set title of chat window
        self.window_chat.set_title(nickname)

        #refersh
        self.window_chat.update()

        #show the chat window and hide login window
        self.window_chat.deiconify()
        self.window.withdraw()
    def send_chat_data(self):
        #get message in the input box and send it to the server
        #get message
        message= self.window_chat.get_inputs()
        #clear the input box
        self.window_chat.clear_input()
        #join message together and wrappe it
        request_text=RequestProtocol.request_chat(self.username,message)
        #send the message
        self.conn.send_data(request_text)
        #show the message client send in chat window

        self.window_chat.append_message('me',message)
    def response_chat_handle(self,response_data):

        #receive the chat response by server
        sender=response_data['nickname']
        message=response_data['message']
        self.window_chat.append_message(sender,message)
    def exit(self):
        #exit program
        self.is_running =False
        self.conn.close()
        sys.exit(0)


if __name__ == '__main__':
    client=Client()
    client.startup()