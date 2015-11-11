#!/usr/bin/env python
import socket
import sys
import collections
import time
import Queue
import threading

from threading import Thread
from SocketServer import ThreadingMixIn
 
class ClientThread(Thread):
 
    def __init__(self,socket,ip,port):
        Thread.__init__(self)
        self.socket = socket
        self.ip = ip
        self.port = port
        print "New thread started"
      
       
 
 
    def run(self):
        

           
        status = 0   
        userpresent = 0     
        while True:
            self.socket.send(str(TIME_OUT))
            data2 = "successful"
            while userpresent == 0:
                num = 0
                userdata = self.socket.recv(2048)
                
               
                if not userdata: break
    
                line = open('user_pass.txt').readlines() 
                for userpass in line:
                    user = userpass.split(" ")
                    if userdata == user[0]:
                        userpresent = 1
                if userpresent == 0:        
                        
                    data2 = "invalid login"
                    status = 0
                    print data2
                    self.socket.send(data2)
                    
                    continue
                else:
                    
                    for p in blockusers:
                        print "blockusers: " , p
                        val = p.partition(" ")
                        valin = val[2].partition(" ")
                        curtime =time.time()
                        if val[0] == userdata and float(valin[0]) >= curtime - BLOCK_TIME and valin[2] == str(ip):     #Blocktime and ip
                            data2 = " blocked "
                            status = 2
                            
                    for p in curusers:
                        print "curusers:", p
                        if userdata == p:
                            data2 = "same user"
                            status = 1
                            print data2
                    if data2 == " blocked ":
                    
                        self.socket.send(data2)
                        status = 2
                    elif data2 == "same user":
                        self.socket.send(data2)
                        status = 1
                        
                    
            if data2 == "successful":
                self.socket.send(data2)
                passpresent = 0
                while status == 0:
                    passdata = self.socket.recv(2048)
                    validity = userdata + " " + passdata
                    
                    if (validity not in open('user_pass.txt').read()):  
                        data2 = "invalid password"
                        print data2   
                        num = num + 1       
                        if num == 3:
                            status = 2
                            self.socket.send(data2)
                            print "breaking"
                            break
                                    
                                    
                        else: 
                            status = 0 
                            
                           
                            self.socket.send(data2)
                            
                    else:
                        data2 = "successful"
                        self.socket.send(data2)
                        for p in offlineusers:
                            t = p.partition(" ")
                            if t[0] == userdata:
                                lock.acquire()
                                offlineusers.remove(p)
                                lock.release()
                       
                        lock.acquire()        
                        curusers.append(userdata)
                        lock.release()
                        print userdata + " logged in"
                        status = 1  # 0 for offline , 1 for online , 2 for blocked 
                        logtime=time.time()
                        fd = self.socket.fileno()
                        userfd = userdata + " " + str(fd)
                        lock.acquire()
                        userfdmap.append(userfd)
                        lock.release()
                               
                        
                             
                            
                            
            
           # print "[+] thread ready for "+ip+":"+str(port)
            if (status == 2 and num == 3):
                blockuserdata = userdata + " " + str(time.time()) + " " + str(ip)
                blockusers.append(blockuserdata)
                fd = self.socket.fileno()
                lock.acquire()
                del sendqueues[fd]
                lock.release()
                print blockuserdata, " blocked for 60 seconds"
                sys.exit()
                
                
            else:
                
                while True:     
                    self.socket.settimeout(TIME_OUT)
                    command = self.socket.recv(2048)
                    if "send " in command:
                        content = command.partition(" ")
                        contentinner = content[2].partition(" ")
                        sendmsg = userdata + ": " + contentinner[2]
                      
                        receiver = contentinner[0]
                        errorflag = 1
                       
                        
                        for z in userfdmap:
                            zi = z.partition(" ")
                            if zi[0] == receiver:
                                receiverfd = int(zi[2])
                                
                                errorflag = 0
                                lock.acquire()
                                sendqueues[receiverfd].put(sendmsg)
                                lock.release()
                        
                                
                                
                        if errorflag == 1:
                            replymsg = "User is offline.  Don't worry , we will get it delivered."     #offline messaging 
                            file = open('{0}.txt'.format(receiver),"a+")
                            localtime = time.asctime( time.localtime(time.time()) )
                            sendmsg = sendmsg + " " + "on" + " " + localtime
                            file.write(sendmsg)
                            file.write("\n")
                            file.close()
                            
                        else:
                            
                            replymsg = "message sent"
                            
                        self.socket.send(replymsg)
                            
                    elif "broadcast user" in command:
                        content = command.split(" ")
                        receivers = []
                        messageflag = 0
                        sendmessage = userdata + ":" 
                        for i, val in enumerate(content):
                            if ( i != 0 or i != 1):
                                if val != "message" and messageflag == 0:
                                    receivers.append(val)
                                elif val == "message":
                                    i = i + 1 
                                    messageflag = 1
                                elif messageflag == 1:
                                    sendmessage = sendmessage + " " + val 
                                    
                                
                            
                                        
                               
                        for p in receivers:
                            print p
                            errorflag = 1 
                            for z in userfdmap:
                                zi = z.partition(" ")
                                if p == zi[0]:
                                    receiverfd = int(zi[2])
                                    print receiverfd
                                    errorflag = 0
                                    lock.acquire()
                                    sendqueues[receiverfd].put(sendmessage)
                                    lock.release()
                        if errorflag == 1:
                            
                            replymsg = "Cannot broadcast message to all , few users offline"
                        else:
                            replymsg = "message broadcasted"
                            self.socket.send(replymsg)              
                                          
                          
                                
                    elif command == "inbox":
                             sendmsg = ""
                             file = open('{0}.txt'.format(userdata),"r")
                             file.seek(0)
                             first_char = file.read(1)
                             if not first_char:
                                 sendmsg = "Your Inbox is empty"
                             else:
                                 file.seek(0)     
                                 for msg in file:
                                     sendmsg = sendmsg + "\n" + msg
                             self.socket.send(sendmsg)      
                        
                                    
                                
                                
                                
                   
       
                    elif command == "whoelse":
                        online = " "
                        for p in curusers:
                        
                            if p != userdata:
                                online = online + p + " "
                        self.socket.send(online)  
                    elif "wholast" in command :
                        div = command.partition(" ")
                        print div[0]
                        print div[2]
                        lastnumber = int(div[2])*60
                        #lastnumber = float(lastnumber)*60.0
                        offline = " "
                        for p in offlineusers:
                            print p
                            t = p.partition(" ")
                            curtime = time.time()
                            if ( curtime - float(lastnumber) ) <= float(t[2]):
                                offline = offline + t[0] + " "
                        
                        self.socket.send(offline)  
                    elif command == "logout":        
                        curusers.remove(userdata)
                        offlinedata = userdata + " " + str(logtime)
                        lock.acquire()
                        offlineusers.append(offlinedata)
                        lock.release()
                        print offlinedata , "removed"
                        logoutack = "logged out" 
                        self.socket.send(logoutack)
                        print "[+] thread disconnected for "+ip+":"+str(port)
                        fd = self.socket.fileno()
                        lock.acquire()
                        del sendqueues[fd]
                        userfdmap.remove(userfd)
                        lock.release()
                        sys.exit()
                    
                    elif "broadcast message" in command:
                          message = command.partition(" ")
                          messagef = message[2].partition(" ")
                          
                          msg = userdata + ": " + messagef[2]
                          lock.acquire()
                          for  q in sendqueues.values():
                              q.put(msg)
                          lock.release()      
                          ack = "broadcasted"      
                          self.socket.send(ack)
                    else:
                          error = "Invalid command. Please enter a proper one"
                          self.socket.send(error)
                                      
                          
                          
        lock.acquire()    
        curusers.remove(userdata) 
        lock.release()       
        offlinedata = userdata + " " + str(logtime)
        lock.acquire()
        offlineusers.append(offlinedata)
        lock.release()
        print offlinedata , "removed"
        print "logged out"
        sys.exit()
        
class ClientThreadread(Thread):
    def __init__(self,sock):
        Thread.__init__(self)
        
        self.sock = sock
        
        print "New thread for chat relying started"
       
       
       
      
       
 
 
    def run(self):
         
         
         tcpsock2.listen(1)
         (conn2, addr) = tcpsock2.accept()
         welcomemsg = "hi"
         conn2.send(welcomemsg)
         chat = "initial"
         print "ind here is"
         print self.sock.fileno()
         while True:
             for p in userfdmap:           #userfdmap contains mapping between usernames and their socket's file despcriptor which we use as index to access their respective queue
                 if str(self.sock.fileno()) in p:
                     connectionpresent = 1
                 else:
                     connectionpresent = 0         #We will use this to implement other features - no use as of now
                 
            
             
             try:
                 chat = sendqueues[self.sock.fileno()].get(False)
                
                 print chat
                 conn2.send(chat)     
             except Queue.Empty:
                
                 chat = "none" 
                 time.sleep(2)
             except KeyError, e:
                 pass
                     
                   
            
         
                      
             
            
         
        
         
    
            

                    
 
    
lock = threading.Lock()  
global command
command = ""                

sendqueues = {}        
TCP_IP = '0.0.0.0'
TCP_PORT = int(sys.argv[1])
TCP_PORT2 = 125
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
TIME_OUT = 1800.0 #seconds   - For time_out    Block_time is 60 seconds
BLOCK_TIME = 60.0



curusers = [] 
offlineusers = []
blockusers = []
userlog = {}
userfdmap = []

 
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#host = socket.gethostname()
tcpsock.bind(('', TCP_PORT))

tcpsock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock2.bind(('', TCP_PORT2))
         

threads = []
 
while True:
    tcpsock.listen(6)
    print "Waiting for incoming connections..."
    (conn, (ip,port)) = tcpsock.accept()
    q = Queue.Queue()
    lock.acquire()
   
   
    sendqueues[conn.fileno()] = q
    lock.release()
    
           
    print "new thread with " , conn.fileno()
    newthread = ClientThread(conn,ip,port)
    newthread.daemon = True
    newthread.start()
    newthread2 = ClientThreadread(conn)
    newthread2.daemon = True
    
    newthread2.start()
    threads.append(newthread)
    threads.append(newthread2)
    
    
 
for t in threads:
    t.join()
    
    print "eND"
