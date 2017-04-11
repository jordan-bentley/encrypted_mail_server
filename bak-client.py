# Messaging Client
import socket
import sys
import Crypto
from Crypto.PublicKey import RSA
#import getpass


MSGLEN = 1

# CONTRACT
# get_message : socket -> string
# Takes a socket and loops until it receives a complete message
# from a client. Returns the string we were sent.
# No error handling whatsoever.
def receive_message (sock):
  chars = []
  try:
    print "1"
    while True:
      print "2"
      char = sock.recv(1)
      print "3"
      if char == b'\0':
        print "3"
        break
      if char == b'':
        print "4"
        break
      else:
        print "5"
        # print("Appending {0}".format(char))
        chars.append(char.decode("utf-8") )
        print "6"
  finally:
    return ''.join(chars)
  
def send (msg):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((HOST, PORT))
  length = sock.send(bytes(msg + "\0"))
  print ("SENT MSG: '{0}'".format(msg))
  print ("CHARACTERS SENT: [{0}]".format(length))
  return sock

def recv (sock):
  response = receive_message(sock)
  print("RESPONSE: [{0}]".format(response))
  sock.close()  

def send_recv (msg):
  recv(send(msg))
  
def encrypt(key, msg):
    encrypt_msg = key.encrypt(msg)
    return encrypt_msg

if __name__ == "__main__":
  # Check if the user provided all of the 
  # arguments. The script name counts
  # as one of the elements, so we need at 
  # least three, not fewer.
  if len(sys.argv) < 3:
    print ("Usage:")
    print (" python client.py <host> <port>")
    print (" For example:")
    print (" python client.py localhost 8888")
    print 
    sys.exit()

  HOST = sys.argv[1]
  PORT = int(sys.argv[2])
  print "1"
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print "2"

  sock.connect((HOST, PORT))
  print "3"

  sock.send(b"HELO\0")
  print "4"

  answer = receive_message(sock)
  print "5"

  print("RESPONSE: [{0}]".format(answer))
  pub_key = ""
  print "6"

  if answer == "OLEH":
    print "7"

    sock.send(b"REQ_KEY\0")
    pub_key = receive_message()
    print("RESPONSE: [{0}]".format(pub_key))
  #socklength = sock.send(b"DUMP\0")
  #print ("CHARACTERS SENT: [{0}]".format(length))
  #response = receive_message(sock)
  #print("RESPONSE: [{0}]".format(response))
  sock.close()

  # I don't want to copy paste everything above.
  # So, I put it in a function or two.
  
  # alive = True
  # logged_in_user = None
  # print 'Type "HELP" for a list of commands.'
  # while alive:
  #   if loged_in_user != None:
  #     msg = raw_input("> ")
  #   else:
  #     msg = "LOGIN" + raw_input("Login: ") + raw_input("Password: ")
  #   if msg.lower() == "help":
  #     print "Commands:\nREGISTER <username>\nMESSAGE <TO: username> <message>\nCOUNT <username>\n"
  #   elif msg.split(" ")[0].lower() == 'register':
  #     s = send(msg)
  #     public_johnson = recv(s)
  #   else:
  #     s = send(logged_in_user, encrypt(public_johnson, msg))
  #     recv(s)
  

  
 # send_recv("DUMP")

 # send_recv("STORE <jadudm>")

 #
 #  recv(send("DUMP"))
 #  #recv(send("GETMSG jadudm"))
 #  #recv(send("DELMSG jadudm"))