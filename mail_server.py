import socket
import sys
import Crypto
import hashlib

from Crypto.PublicKey import RSA
from Crypto import Random


class Server(object):
    def init(self):
        self.priv_key = None
        self.pub_key = None
        self.MBX = {}
        self.IMQ = []
        self.USR = {}
        self.PKEYS = {}  
        
        
    # CONTRACT
    # start_server : string number -> socket
    # Takes a hostname and port number, and returns a socket
    # that is ready to listen for requests
    def start_server (self, host, port):
      self.priv_key, self.pub_key = self.create_keys()
      print ("Keys generated")
      server_address = (host, port)
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.bind(server_address)
      sock.listen(1)
      return sock
      
    def create_keys(self):
      random_generator = Random.new().read
      private = RSA.generate(1024, random_generator)
      public = private.publickey()
      return (private, public)
      
    # CONTRACT
    # get_message : socket -> string
    # Takes a socket and loops until it receives a complete message
    # from a client. Returns the string we were sent.
    # No error handling whatsoever.
    def get_message (self, sock):
      chars = []
      connection, client_address = sock.accept()
      print ("Connection from [{0}]".format(client_address))
      try:
        while True:
          char = connection.recv(1) 
          if char == b'\0':
            break
          if char == b'':
            break
          else:
            # print("Appending {0}".format(char))
            chars.append(char.decode("utf-8") )
      finally:
        return (''.join(chars), connection)
        
    def decrypt(self, msg):
      encrypted = eval(msg)
      d_msg = self.priv_key.decrypt(encrypted)
      return d_msg
    
    # CONTRACT
    # socket -> boolean
    # Shuts down the socket we're listening on.
    def stop_server (self, sock):
      return sock.close()
    
    # CONTRACT
    # string -> SHA1
    # produces a sha1 checksum form a string
    def sha_1(self, string):
      sha = hashlib.sha1()
      sha.update(string)
      return sha.hexdigest()
    
    # CONTRACT
    # string -> boolean
    # Takes an unencrypted string with sha1 appended and verifys the checksum
    def checksum(self, string):
      sha = string[-40:]
      msg = self.removeChecksum(string)
      if self.sha_1(msg) == sha:
        return True
      else:
        return False
        
    def removeChecksum(self, string):
      return string[:-40]
    
    # DATA STRUCTURES
    # The structures for your server should be defined and documented here.
    
    # SERVER IMPLEMENTATION
    # The implementation of your server should go here.
    
    # CONTRACT
    def handle_message (self, msg):
      if "HELO" == msg:
        print("Hello recieved.")
        print("Returning Public Key")
        #Sends back the 'okay' msg to the client and gives the public key
        #for encryption of login data
        return("KEY", self.pub_key)
      else:
        msgChecksum = self.decrypt(msg)
        print "MSG+CHECKSUM: "+msgChecksum
        msg = self.removeChecksum(msgChecksum)
        print "MSG: "+msg
    
        action = msg.split(" ")[0].upper()
        if self.checksum(msgChecksum) == False:
          return("SEND", "Resend")
        if "TEST" == action:
          print ("It Worked")
          return ("OK", msg)
        
        elif "DUMP" == action:
          print("Mailbox: ")
          print(self.MBX)
          print("Message Queue: ")
          print (self.IMQ)
          print("User Dictionary: ")
          print(self.USR)
          return ("SEND", "Dumped.")
          
        elif "REGISTER" == action:
          # Get the username
          username = msg.split(" ")[1]
          password = msg.split(" ")[2]
          # Create an empty list of messages
          self.MBX[username] = []
          self.USR[username] = self.pub_key.encrypt(password, 32)
          # Encrypt this password ^^ 
          u_priv, u_pub = self.create_keys()
          self.PKEYS[username] = u_priv
          return ("KEY", u_pub)
        elif "LOGIN" == action:
          username = msg.split(" ")[1]
          password = msg.split(" ")[2]
          if self.USR[username] == self.pub_key.encrypt(password, 32):
            u_priv = self.PKEYS.get(username)
            u_pub = u_priv.publickey()
            return("KEY", "OK")
          else:
            return("SEND", "KO")
            
        elif "MESSAGE" == action:
          # Get the content; slice everything after
          # the word MESSAGE
          content = msg.split(" ")[1:]
          # Put the content back together, and put 
          # it on the incoming message queue.
          self.IMQ.insert(0, " ".join(content))
          return ("SEND", "Sent message.")
          
        elif "STORE" == action:
          username = msg.split(" ")[1]
          queued = self.IMQ.pop()
          print("Message in queue:\n---\n{0}\n---\n".format(queued))
          self.MBX[username].insert(0, queued)
          return ("SEND", "Stored message.")
          
        elif "COUNT" == action:
          username = msg.split(" ")[1]
          return ("SEND", "COUNTED {0}".format(len(self.MBX[username])))
          
        elif "DELMSG" == action:
          username = msg.split(" ")[1]
          self.MBX[username].pop(0)
          return ("OK", "Message deleted.")
          
        elif "GETMSG" == action:
          username = msg.split(" ")[1]
          first = self.MBX[username][0]
          print ("First message:\n---\n{0}\n---\n".format(first) )
          return ("SEND", first)
          
        else:
          print("NO HANDLER FOR CLIENT MESSAGE: [{0}]".format(msg))
          return ("KO", "No handler found for client message.")
