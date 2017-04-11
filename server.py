#
# https://pymotw.com/2/socket/tcp.html
# https://docs.python.org/3/howto/sockets.html

# Messaging Server v0.1.0
import socket
import sys
import Crypto
import hashlib

from Crypto.PublicKey import RSA
from Crypto import Random


priv_key = None
pub_key = None
# CONTRACT
# start_server : string number -> socket
# Takes a hostname and port number, and returns a socket
# that is ready to listen for requests
def start_server (host, port):
  global priv_key, pub_key
  priv_key, pub_key = create_keys()
  print ("Keys generated")
  server_address = (host, port)
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(server_address)
  sock.listen(1)
  return sock
  
def create_keys():
  random_generator = Random.new().read
  private = RSA.generate(1024, random_generator)
  public = private.publickey()
  return (private, public)
  
# CONTRACT
# get_message : socket -> string
# Takes a socket and loops until it receives a complete message
# from a client. Returns the string we were sent.
# No error handling whatsoever.
def get_message (sock):
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
    
def decrypt(msg):
  encrypted = eval(msg)
  d_msg = priv_key.decrypt(encrypted)
  return d_msg

# CONTRACT
# socket -> boolean
# Shuts down the socket we're listening on.
def stop_server (sock):
  return sock.close()

# CONTRACT
# string -> SHA1
# produces a sha1 checksum form a string
def sha_1(string):
  sha = hashlib.sha1()
  sha.update(string)
  return sha.hexdigest()

# CONTRACT
# string -> boolean
# Takes an unencrypted string with sha1 appended and verifys the checksum
def checksum(string):
  sha = string[-40:]
  msg = removeChecksum(string)
  if sha_1(msg) == sha:
    return True
  else:
    return False
    
def removeChecksum(string):
  return string[:-40]

# DATA STRUCTURES
# The structures for your server should be defined and documented here.

# SERVER IMPLEMENTATION
# The implementation of your server should go here.
MBX = {}
IMQ = []
USR = {}
PKEYS = {}

# CONTRACT
def handle_message (msg):
  if "HELO" == msg:
    print("Hello recieved.")
    print("Returning Public Key")
    #Sends back the 'okay' msg to the client and gives the public key
    #for encryption of login data
    return("KEY", pub_key)
  else:
    msgChecksum = decrypt(msg)
    print "MSG+CHECKSUM: "+msgChecksum
    msg = removeChecksum(msgChecksum)
    print "MSG: "+msg

    action = msg.split(" ")[0].upper()
    if checksum(msgChecksum) == False:
      return("SEND", "Resend")
    if "TEST" == action:
      print ("It Worked")
      return ("OK", msg)
    
    elif "DUMP" == action:
      print("Mailbox: ")
      print(MBX)
      print("Message Queue: ")
      print (IMQ)
      print("User Dictionary: ")
      print(USR)
      return ("SEND", "Dumped.")
      
    elif "REGISTER" == action:
      # Get the username
      username = msg.split(" ")[1]
      password = msg.split(" ")[2]
      # Create an empty list of messages
      MBX[username] = []
      USR[username] = pub_key.encrypt(password, 32)
      # Encrypt this password ^^ 
      u_priv, u_pub = create_keys()
      PKEYS[username] = u_priv
      return ("KEY", u_pub)
    elif "LOGIN" == action:
      username = msg.split(" ")[1]
      password = msg.split(" ")[2]
      if USR[username] == pub_key.encrypt(password, 32):
        u_priv = PKEYS.get(username)
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
      IMQ.insert(0, " ".join(content))
      return ("SEND", "Sent message.")
      
    elif "STORE" == action:
      username = msg.split(" ")[1]
      queued = IMQ.pop()
      print("Message in queue:\n---\n{0}\n---\n".format(queued))
      MBX[username].insert(0, queued)
      return ("SEND", "Stored message.")
      
    elif "COUNT" == action:
      username = msg.split(" ")[1]
      return ("SEND", "COUNTED {0}".format(len(MBX[username])))
      
    elif "DELMSG" == action:
      username = msg.split(" ")[1]
      MBX[username].pop(0)
      return ("OK", "Message deleted.")
      
    elif "GETMSG" == action:
      username = msg.split(" ")[1]
      first = MBX[username][0]
      print ("First message:\n---\n{0}\n---\n".format(first) )
      return ("SEND", first)
      
    else:
      print("NO HANDLER FOR CLIENT MESSAGE: [{0}]".format(msg))
      return ("KO", "No handler found for client message.")




if __name__ == "__main__":
  # Check if the user provided all of the 
  # arguments. The script name counts
  # as one of the elements, so we need at 
  # least three, not fewer.
  if len(sys.argv) < 3:
    print ("Usage: ")
    print (" python server.py <host> <port>")
    print (" e.g. python server.py localhost 8888")
    print 
    sys.exit()

  host = sys.argv[1]
  port = int(sys.argv[2])
  sock = start_server(host, port)
  print("Running server on host [{0}] and port [{1}]".format(host, port))
  
  RUNNING = True
  while RUNNING:
    message, conn = get_message(sock)
    print("MESSAGE: [{0}]".format(message))
    result, msg = handle_message(message)
    print ("Result: {0}\nMessage: {1}\n".format(result, msg))
    if result == "OK":
      conn.sendall(bytes("{0}\0".format(result)))
    elif result == "SEND":
      conn.sendall(bytes("{0}\0".format(msg)))
    elif result == "KEY":
      conn.send(pub_key.exportKey())
      #conn.sendall(msg)
    else:
      print("'else' reached.")
      RUNNING = False
    conn.close()

    
  stop_server(sock)