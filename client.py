#!/usr/bin/env python
import sys
import socket
import time
import threading
from threading import Thread
from SocketServer import ThreadingMixIn




class ServerThread(Thread):
 
    def __init__(self,socket):
        Thread.__init__(self)
        self.socket = socket
        
     #   print "New thread started for write"
        
        
 
 
    def run(self):
        print "send" 
        
        while True:
            starttime = time.time()
        
            
            command = raw_input(" Enter command: ")
            
            
                
            curtime = time.time()
        
            if  curtime - starttime > float(TIME_OUT):     #Client tiems itself out after TIME_OUT idle time
                print " Your session has been timed out! Please log in again :(" 
                self.socket.close()
                sys.exit()
            else: 
                
                self.socket.send(command)
           
                ack = self.socket.recv(BUFFER_SIZE)
                print ack
                if ack == "logged out":
                    log = 1
                    self.socket.close()
                    sys.exit()
                    
                elif ack == "user already exists":
                    print "user alread exists -.-"  
                    self.socket.close()
                    sys.exit()
          
             
               
                
                
                            
      
        
        
class ServerThreadread(Thread):
 
    def __init__(self,socket):
        Thread.__init__(self)
        self.socket = socket
        
      #  print "New thread started for chat display"
      
       
 
 
    def run(self):
        
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.connect((TCP_IP, TCP_PORT2))
        welcomemsg = s2.recv(BUFFER_SIZE)
        chat = "initial"
        print welcomemsg
        
        while True:
            if log == 0:
              #  print "inside loop"
                chat=s2.recv(BUFFER_SIZE)
                print chat
                time.sleep(5)
                
            if log == 1:
              #  print "going to exit"
                s2.close()
                sys.exit() 
       
           
                              
        


 
 
TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
TCP_PORT2 = 125
BUFFER_SIZE = 1024
threads = []
global log
log = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
TIME_OUT = s.recv(BUFFER_SIZE)   #Server exchanges tmeout details with client at the start of every socket
count = [1, 2, 3]
status = 0
while status == 0:
    number = 0
    username = raw_input("Enter username: ")
    s.send(username)
    usernamecheck = s.recv(BUFFER_SIZE)
    if ( usernamecheck == "invalid login" ):
        print "Invalid username , enter details again "
        status =0
        
        continue
    else:
        if usernamecheck == " blocked ":
            status = 2
            print "I said you have been blocked for 60 seconds. Be patient -.-"
            sys.exit()
        elif usernamecheck == "same user":
            status = 1
            print "User is already online. Who are you ?"
            sys.exit()
        else:    
            while status == 0:
                password = raw_input("Enter password: ") 
                s.send(password)
                passwordcheck = s.recv(BUFFER_SIZE)
                if ( passwordcheck == "invalid password" ):
                    
                    status = 0
                    number = number + 1
                    if number == 3:
                        status = 2    
                        break
                
                    else:
                        print " Invalid password , enter details again "
                        continue
                else:
                    status = 1        
                        
                           
if number == 3 and status == 2:
    print "I don't know. My instructor has asked me to block you for 60s." 
    sys.exit()
            
         

        
if ( status == 1 ):
    print "logged in"
    try:
    
        newthread = ServerThread(s)
        newthread.daemon = True
        newthread2 = ServerThreadread(s)
        newthread2.daemon = True
        newthread.start()
        newthread2.start()
        threads.append(newthread)
        threads.append(newthread2)
        while True:
            for t in threads:
                t.join(600)
                if not t.isAlive():
                    break
            break        
            
            
    except KeyboardInterrupt:
        command = "logout"
        s.send(command)
        sys.exit()
    
   
            
    

 

