CLIENT sends "HELO" to the server                                   DONE
Server Reads it and returns "OLEH".                                 DONE

If sucess, client sends a request for the public_key                DONE
server sends public_key to client                                   DONE

client prompted for register or login                               DONE
credentials are encrypted with public_key and sent to the server    DONE

Server generates a new set of keys USR[username] = user_private_key DONE
Server sends the client their public_key (Stored on client)         DONE
    
All messages are encrypted with public_key on client                DONE
decrypted on server with private key                                DONE
    
All messages include the username                                   CAN IMPLEMENT

---------------------------------------------------------------------------------

Changes for Proxy Server:

Psuedo-code for SHA implementation.

CLIENT:
msg = keyboard_input
cheksum = SHA1(msg)
msgwithSHA = msg + checksum
encrypted_msg = encrypt(msgWithSHA)
send(encrypted_msg)

SERVER:
encrypted_msg = receive(client)
msgWithSHA = decrypt(encrypted_message)
checksum = getSHAfromMsg(msgWithSHA)
msg = getMsgFromMsg(msgWithSHA)
if SHA1(msg) == checksum:
    print "data verified legit"
else:
    print "Data corrupt"
    askClientToTryAgain()
    
TODO:

Client takes the already encrypted message, breaks it into chunks (size TBD)

Client calculates the SHA of each chunk and sends the the chunks inidividually
with their SHA values.

Server recieves each chunk and calculates the SHA for it. If it matches
the SHA that was sent with the chunk, it accepts and stores/appends the values
until the Client has finished sending chunks.

If the SHA values do not match, the Server returns a KO (or something) which
tells the client to resend that piece of data. This will continue to occur until
the SHA values match.

Server will need to send back an OK or KO for each chunk to tell the client
what to do next. If OK the client sends the next chunk, if KO client resends
the previous chunk.

