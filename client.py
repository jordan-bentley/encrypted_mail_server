# Messaging Client
import socket
import sys
import hashlib

from Crypto.PublicKey import RSA


MSGLEN = 1
KEY = None
# CONTRACT
# get_message : socket -> string
# Takes a socket and loops until it receives a complete message
# from a client. Returns the string we were sent.
# No error handling whatsoever.
def receive_message (sock):
  chars = []
  try:
    while True:
      char = sock.recv(1)
      if char == b'\0':
        break
      if char == b'':
        break
      else:
        # print("Appending {0}".format(char))
        chars.append(char.decode("utf-8") )
  finally:
    return ''.join(chars)

# CONTRACT
# string -> SHA1
# produces a sha1 checksum form a string
def sha_1(string):
  sha = hashlib.sha1()
  sha.update(string)
  return sha.hexdigest()

def send (msg):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((HOST, PORT))
  length = sock.send(bytes(str(msg) + "\0"))
  print ("SENT MSG: '{0}'".format(msg))
  print ("CHARACTERS SENT: [{0}]".format(length))
  return sock

def recv_key (sock):
  key = sock.recv(1024)
  get_key(key)
  sock.close()

def recieve (sock):
  response = receive_message(sock)
  sock.close()  
  return response


def send_recv (msg):
  recieve(send(msg))
  
def get_key(key):
  global KEY
  #Error handling for bit loss here
  KEY = RSA.importKey(key)
  print KEY
  
def control():
  msg = raw_input("> ")
  sha = sha_1(msg)
  print "SHA: "+ sha
  encrypted_msg = KEY.encrypt(msg+sha, 32)
  print encrypted_msg
  s = send(encrypted_msg)
  recieved_msg = recieve(s)
  while recieved_msg == "Resend":
    s = send(encrypted_msg)
    recieved_msg = recieve(s)
  print("RESPONSE: [{0}]".format(recieved_msg))


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


  s = send("HELO")
  recv_key(s)
  
  on = True
  logged_in_user = False
  while on:
    while logged_in_user == False:
      ans = (raw_input("Login or Register? l/r \n >"))
      if ans.lower() == "l" or ans.lower() == 'login':
        print ("Please login using your credentials.\n")
        username, password = [raw_input("Username: "), raw_input("Password: ")]
        msg = "LOGIN " + username + " " + password
        encrypted_msg = KEY.encrypt(msg+sha_1(msg), 32)
        s = send(encrypted_msg)
        recv_key(s)
        logged_in_user = True
      elif ans.lower() == "r" or ans.lower() == 'register':
        while logged_in_user == False:
          print ("Please register a username and password.\n")
          username, password, confirm_password= [raw_input("Username: "), raw_input("Password: "), raw_input("Confirm password: ")]
          if password == confirm_password:
            msg = "REGISTER " + username + " " + password
            encrypted_msg = KEY.encrypt(msg+sha_1(msg), 32)
            s = send(encrypted_msg)
            recv_key(s)
            logged_in_user = True
          else: 
            print "Passwords do not match. Try again."
      else:
        print "<{0}> is not a valid command.".format(ans)
    while logged_in_user == True:
      control()
  



 #
 #  recv(send("DUMP"))
 #  #recv(send("GETMSG jadudm"))
 #  #recv(send("DELMSG jadudm"))