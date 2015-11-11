README:

A. Code Description :  

The program uses multi threading concept. There are two scripts , one running on the server side , the other on the client side as it is with every chat server. The server relays the messages. The server side script accepts connections and creates ?2 threads ? for every client that connects 
(i) To process and respond to the who , wholast , send , broadcast commands to the client
(ii) To keep sending the messages that are destined to the client.


Similarly the client uses two threads , one for prompting commands from commands  from user and getting inputs. The other thread  receives chat messages from the server and displays them.  Note : The responses for the commands are received in thread1 

Each pair of thread is connected by a separate socket. (2 sockets are used per client-server) 
One socket between server and client is exclusively used for the server to get the messages from the client?s message queue and send it to the client thread that receives the chat messages.

Shared queues are used. When a connection occurs , a queue is added to the set of queues with the index being the file descriptor of the connection. Hence every client has a separate index and therefore a separate queue in the server. All queues belong to the set sendqueue. 
A message intended for the client is put into the respective queue and the other thread is responsible for taking these messages out of the queue and send it to the appropriate client.

Every queue access is wrapped up in a mutex lock to prevent clashes or race condition

Common lists are used to store the information of online users , blocked users , offline users and mapping between username and the file descriptor to access the sendqueue.

B. Development environment :
Mac OS X
Bash shell
Python 3
Editor used : Textpad
 
C. How to run the code ? 
There are only two scripts. Place them on the different systems. If same systems use 127.0.0.1 as the address. 
Server is invoked from the terminal as
Python server.py <port number>

Client is invoked from the terminal as 
Python client.py <TCP ip address of the server> <port number>
D. Commands to use :
1. whoelse  displays other users who are online

2. wholast lastnumber displays the users who were online until lastnumber minutes ago
3. send <user> <message> sends <message> to <user>
4. Broadcast message displays message to the users who are online
5. Broadcast user <list of users> message broadcasts the message to list of users
6. Inbox  - Shows the messages that were sent when the client was offline. It also shows chat history.

Offline messaging implementation : The offline messaging system works in such a way that it stores the offline messages on a file that is allocated to the client. (Every client has a text file which has their respective chat history)  The inbox command makes the server retrieve command from the file and send it across the client.
P.s : File system is used instead of queue because queue cannot show history.Also offline messages is not available for broadcasted messages. Broadcast is generally done only to those who are online 

P.P.S : The chat messages gets displayed without any proper alignment on the terminal screen. Sometimes they might clash with the command prompt. 







