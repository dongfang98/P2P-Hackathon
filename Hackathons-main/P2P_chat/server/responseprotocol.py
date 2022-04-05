from config import *

#In this part we can emphasize the interactive mode between server and client
#server: get request form client -> handle it -> return the result to client
#client: send the request -> accept the response of sever to judge whether success or not
#protocol is used to wrappe the message

class ResponseProtocol(object):
  def response_login_result(result,nickname,username):
    return DELIMITER.join([RESPONSE_LOGIN_RESULT,result,nickname,username])

  def response_chat(nickname,messages):
    return DELIMITER.join([RESPONSE_CHAT,nickname,messages])