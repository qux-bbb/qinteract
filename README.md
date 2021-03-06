## Intro
1. Automatic interaction with a console program
2. Automatic interaction with a socket


## Install
```
pip install qinteract
```


## Example
### ProcessInteraction
Program to be called (want_right.py):  
```python
# coding:utf8
# python3

import random

first_num = str(random.randint(0, 10))
second_num = str(random.randint(0, 10))

first_input = input('input {}: '.format(first_num))
second_input = input('input {}: '.format(second_num))

if first_num==first_input and second_num==second_input:
    print('Right!')
else:
    print('Wrong!')
```

Interaction:  
```python
# coding:utf8
# python3

from qinteract import ProcessInteraction

command = ['python', 'want_right.py']

pi = ProcessInteraction(command)
for i in range(2):
    content = pi.recvuntil_re(r'input (\d+): ')
    print(content[0])
    num = content[1].group(1)
    print(repr(num))
    pi.sendline(num)
content = pi.recvline()
print(content)
```


### SocketInteraction
Server side program (server.py):  
```python
# coding:utf8
# python3

import random
import socket
import sys

# Create socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 9999

# Bind the port
serversocket.bind(('', port))

# Set the maximum number of connections to queue after exceeding
serversocket.listen(5)

while True:
    try:
        print('Wait for connection...')
        # Establish client connection
        clientsocket, addr = serversocket.accept()
        print('Connection address: ', addr)

        first_num = str(random.randint(0, 10))
        second_num = str(random.randint(0, 10))

        clientsocket.send('input {}: '.format(first_num).encode('utf8'))
        first_input = clientsocket.recv(10).decode('utf8').strip()
        clientsocket.send('input {}: '.format(second_num).encode('utf8'))
        second_input = clientsocket.recv(10).decode('utf8').strip()

        print(first_input)
        print(second_input)

        if first_num == first_input and second_num == second_input:
            clientsocket.send('Right!\n'.encode('utf8'))
        else:
            clientsocket.send('Wrong!\n'.encode('utf8'))
        clientsocket.shutdown(socket.SHUT_RDWR)
        clientsocket.close()
    except KeyboardInterrupt as identifier:
        print('The program was stopped manually')
        break

serversocket.close()
```

Interaction：  
```python
# coding:utf8
# python3

from qinteract import SocketInteraction

si = SocketInteraction('127.0.0.1', 9999)
for i in range(2):
    content = si.recvuntil_re(r'input (\d+): ')
    print(content[0])
    num = content[1].group(1)
    print(repr(num))
    si.sendline(num)
content = si.recvline()
print(content)
```