# -*- coding:utf-8 -*-
# LaBox makes answer

import socket

HOST = ''
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)

conn, addr = s.accept()
print('Connected by', addr)

while 1:
    data = conn.recv(1024)
    print('Length: ' + str(len(data)))
    print('Received: ' + str(data))
    if str(data == 'quit':
        print('quit request...')
        break
    conn.send(data)

conn.close()
