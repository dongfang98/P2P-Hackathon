# Hackathon Project -- Peer to Peer Chat Program

This program is designed to function as a multi-user chatroom. To be specific, each user is able to login into the system.  
After login, user can send messages to all other online users and can recieve message from others.  
The project is devided into two parts: the client side is operated by GUI, while the server side recieving incomming requests from clients wanting to communicate. 

## Project Environment 
* Project Name: P2P Chat Program
* Project Mode: C/S
* MacOS, python 3, PyCharm 
* Python GUI, Multithread programming, Network programming, Database programming 

## The Server side
 - This part contains two modules, the connectiong module and the processing module.  
 - The connecting module is used to connect server with clients.  
 - It is based on TCP Connecting and makes use of Socket API. Once program starts, sever will be set to listen module and open for connecting.  
 - The processing module is used to deal with clients' request, each time it recieve a request, sever starts a new thread.  
 - There are two kind of requests, the first kind of request is Login request and the second is chat request.Each can be identified by it's specific request header.  
 - The login request contains client's information: username、password、nickname. Sever will check it's database, see if username and password is legal. If so, it save user's information into a dictionary:  key is username, value is another dictionary whose key is socket number and value is nickname. Then sever will response to client with a success code. If password or username is wrong, sever will return a failed code.  
 - The chatting request contains user's username and message. Sever will check if username is in the dictionary and then check if the socket number is right. To do so, sever knows this request comes from a online user and it will send message to all online users in the dictionary. If the client did not login, sever will return a failed message.  

## The Client side
 - User part can also be devided into connecting part and processing part.  
 - The connecting part uses TCP Connecting protocol and send connecting request to sever socket.  
 - The processing part generate request and send to sever, it also decode respond from sever and return a graphical interface to users.   

## Operations
First to start the server program to get link with the client. Then the client launcher will open the login window.

<img width="886" alt="image" src="https://user-images.githubusercontent.com/78338843/163888688-871bf5cb-65d2-4b5f-af58-24f36adb4d50.png">

Login Success!

<img width="532" alt="image" src="https://user-images.githubusercontent.com/78338843/163888803-793af2c2-56a3-4e05-8940-0309a5902002.png">

Login Failed

<img width="532" alt="image" src="https://user-images.githubusercontent.com/78338843/163888771-6042aee0-fa4d-47e3-9544-c0b6adaaf5fb.png">

After the program login successfully, the user will get into the chat room window.

<img width="907" alt="image" src="https://user-images.githubusercontent.com/78338843/163888912-34bd50ad-c0e4-409f-b778-241cd671e966.png">
<img width="907" alt="image" src="https://user-images.githubusercontent.com/78338843/163889142-c2c8e1fe-9f94-4bae-a0e1-1a7eef4d65a2.png">
<img width="907" alt="image" src="https://user-images.githubusercontent.com/78338843/163889153-1c659a6a-0805-45c8-aaf3-8926245aee8c.png">

Then, the user can enter the message in the input box and send it to other online users. When multiple people getting online, the message will be sent to all online users at the sametime.
