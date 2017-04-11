#
# https://pymotw.com/2/socket/tcp.html
# https://docs.python.org/3/howto/sockets.html

# Messaging Server v0.1.0
import socket
import sys
import Crypto
from Crypto.PublicKey import RSA


priv_key = ""
pub_key = ""

# CONTRACT
# start_server : string number -> socket
# Takes a hostname and port number, and returns a socket
# that is ready to listen for requests
def start_server (host, port):
  priv_key = RSA.generate(1024)
  pub_key = priv_key.publickey()
  print ("Keys generated")
  server_address = (host, port)
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(server_address)
  sock.listen(1)
  return sock
  
  
def register(uname, password):
  LGN[uname] = password
  
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
      char = connection.recv(1024) 
      if char == b'\0':
        break
      if char == b'':
        break
      else:
        # print("Appending {0}".format(char))
        chars.append(char.decode("utf-8") )
  finally:
    return (''.join(chars), connection)

# CONTRACT
# socket -> boolean
# Shuts down the socket we're listening on.
def stop_server (sock):
  return sock.close()

# DATA STRUCTURES
# The structures for your server should be defined and documented here.

# SERVER IMPLEMENTATION
# The implementation of your server should go here.
MBX = {}
IMQ = []
USR = {}
LGN = {}

# CONTRACT
def handle_message (msg):
  if "HELO" in msg:
    return("SEND", "OLEH")
    
  elif "REQ_KEY" in msg:
    return("SEND", pub_key)
  
  elif "DUMP" in msg:
    print(MBX)
    print(IMQ)
    return ("OK", "Dumped.")
    
  elif "REGISTER" in msg:
    # Get the username
    username = msg.split(" ")[1]
    # Create an empty list of messages
    MBX[username] = []
    return ("OK", "Registered.", public_johnson)
    
  elif "MESSAGE" in msg:
    # Get the content; slice everything after
    # the word MESSAGE
    content = msg.split(" ")[1:]
    # Put the content back together, and put 
    # it on the incoming message queue.
    IMQ.insert(0, " ".join(content))
    return ("OK", "Sent message.", None)
    
  elif "STORE" in msg:
    username = msg.split(" ")[1]
    queued = IMQ.pop()
    print("Message in queue:\n---\n{0}\n---\n".format(queued))
    MBX[username].insert(0, queued)
    return ("OK", "Stored message.", None)
    
  elif "COUNT" in msg:
    username = msg.split(" ")[1]
    return ("SEND", "COUNTED {0}".format(len(MBX[username])), None)
    
  elif "DELMSG" in msg:
    username = msg.split(" ")[1]
    MBX[username].pop(0)
    return ("OK", "Message deleted.", None)
    
  elif "GETMSG" in msg:
    username = msg.split(" ")[1]
    first = MBX[username][0]
    print ("First message:\n---\n{0}\n---\n".format(first) )
    return ("SEND", first, None)
    
  else:
    print("NO HANDLER FOR CLIENT MESSAGE: [{0}]".format(msg))
    return ("KO", "No handler found for client message.", None)

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
    print result
    print msg
    print ("Result: {0}\nMessage: {1}\n".format(result, msg))
    if result == "OK":
      if key != None:
        conn.sendall(bytes("{0}\0".format(key)))
      else:
        conn.sendall(bytes("{0}\0".format(result)))
    elif result == "SEND":
      conn.sendall(bytes("{0}\0".format(msg)))
    
    else:
      print("'else' reached.")
      RUNNING = False
    
    conn.close()

    
  stop_server(sock)