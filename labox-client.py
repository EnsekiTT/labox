# -*- coding:utf-8 -*-
# LaBox makes answer
import socket

HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while 1:
    message = input('>')
    utf8_message = message.encode('utf-8')
    s.send(utf8_message)

    if utf8_message == b'quit': break
    data = s.recv(1024)
    print('Received: '+ repr(data))

s.close()
