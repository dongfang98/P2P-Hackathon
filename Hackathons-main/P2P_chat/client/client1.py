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
        #create login window：
        self.window =WindowLogin()
        self.window.on_reset_button_click(self.clear_inputs)
        self.window.on_login_button_click(self.send_login_data)
        #self.window.on_window_close(self.exit)
        #create chat window
        self.window_chat=WindowChat()
        #self.window_chat.on_window_close(self.exit)
        #hide the chat window
        self.window_chat.withdraw()
        #####create the client socket
        self.conn=ClientSocket()

        self.response_handle_function={}
        self.response_handle_function[RESPONSE_LOGIN_RESULT]=self.response_login_handle
        self.response_handle_function[RESPONSE_CHAT]=self.response_chat_handle
        self.window_chat.on_send_button_click(self.send_chat_data)
        #define the global variable and record user name
        self.username=None
        #flag running program
        self.isrunning= True
    def startup(self):
        # Connect the client socket to the server
        self.conn.connect()
        # Since a message may be received at any time, the receiving message should be placed in the thread. 
        # The difference between sever and server is that sever waits for the client response by starting up in a loop. 
        # But each time the loop starts the child thread to see if there are any new user requests that need to be processed. 
        # The client only starts up once (mainloop is an infinite loop).
        #Then we start the response_handle thread directly, enter the response_handle thread and loop through the child thread
        t=Thread(target=self.response_handle)
        t.start()
        # openning the login window is an endless loop, so finally open it
        self.window.mainloop()

    def clear_inputs(self):
        #clean up the window 
        self.window.clear_username()
        self.window.clear_password()
    def send_login_data(self):
        #send the login message(login number and user name) to the server
        #get the typed in password
        username=self.window.get_username()
        password=self.window.get_password()
        # generate request text (encapsulation)
        request_text = RequestProtocol.request_login_result(username,password)
        #send request text to the server
        self.conn.send_data(request_text)


    def response_handle(self):
        #Continuously receive new messages from the processing server（while true +thread）
        #while self.isrunning:
        while True:
          recv_data=self.conn.recv_data()
          #parsing message (one dictionary)
          response_data=self.parse_response_data(recv_data)
          #handle according to the message
          handle_function=self.response_handle_function.get(response_data['response_id'])
          if handle_function:
             handle_function(response_data)

          #if response_data['response_id']==RESPONSE_LOGIN_RESULT:
              #self.response_login_handle(response_data)
          #elif response_data['response_id']==RESPONSE_CHAT:
              #self.response_chat_handle(response_data)
    #no used of self, removed self using static method 
    @staticmethod
    def parse_response_data(recv_data):
        #There are two kinds of messages that need to be processed:
        # 1.Log in response from the server：1001|success|username|user id 
        # or 1001|failure|null
        # 2.Chat server forwarding response：1002|sender's username|message
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
        #login resulr
        print('Login result recieved')
        result = response_data['result']
        if result == '0':
            print('Login Failed')
            #The prompt box displays the title and content
            showinfo('Login result','Login Failed,wrong information!')
            return

        showinfo('Login result','Login Success!')
        nickname=response_data['nickname']
        self.username=response_data['username']
        print('%s has successfully login,nickname is %s'%(self.username,nickname))
        #Sets the title of the chat window
        self.window_chat.set_title(nickname)
        #Habitually refresh
        self.window_chat.update()
        #Display chat window, hide login window
        self.window_chat.deiconify()
        self.window.withdraw()
    def send_chat_data(self):
        #Gets the contents of the input box and sends it to the server
        #Get input
        message= self.window_chat.get_inputs()
        #clear up input box
        self.window_chat.clear_input()
        #Splicing message encapsulation
        request_text=RequestProtocol.request_chat(self.username,message)
        #send message
        self.conn.send_data(request_text)
        #Show the sending message to the chat area:
        self.window_chat.append_message('me',message)
    def response_chat_handle(self,response_data):
        #Get chat message respond from server
        sender=response_data['nickname']
        message=response_data['message']
        self.window_chat.append_message(sender,message)
    def exit(self):
        #exit the program
        self.is_running =False
        self.conn.close()
        sys.exit(0)


if __name__ == '__main__':
    client=Client()
    client.startup()