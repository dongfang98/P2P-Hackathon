from config import *
class RequestProtocol(object):
# this part emphasize the interact mode between server and client
# server aeecpt the request of client and handle it, sand the result to client
# client send request to serve and judge the result by response send by server
# protocol is used to wrap the message send by server

   #function of @staticmethod：
   #class a：
   #def duck():
       #pass
   #@staticmethod
   #def pig():
       #pass
   #t=a()
   #t.duck()
   #t.pig()
   #in this case，t.duck() will show a mistake：TypeError: pig() takes 0 positional arguments but 1 was given
   #Because although there is no parameter, t will be send to duck as self 
   #At this time, we can only call function by a.duck()
   #t.pig() will show no mistake


   @staticmethod
   def request_login_result(username,password):
       return DELIMITER.join([REQUEST_LOGIN,username,password])
   @staticmethod
   def request_chat(username,message):
       return DELIMITER.join([REQUEST_CHAT,username,message])