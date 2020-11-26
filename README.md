## 简单介绍
两个功能：  
1. 和命令行程序的自动化交互
2. 和 socket 的自动化交互


## 安装
```
pip install qinteract
```


## 使用示例
### 命令行自动化交互
待调用程序（want_right.py）：  
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

自动化交互：  
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


### socket自动化交互
服务端程序（server.py）:  
```python
# coding:utf8
# python3

import random
import socket
import sys

# 创建 socket 对象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 9999

# 绑定端口号
serversocket.bind(('', port))

# 设置最大连接数，超过后排队
serversocket.listen(5)

while True:
    try:
        print('等待连接...')
        # 建立客户端连接
        clientsocket, addr = serversocket.accept()
        print("连接地址: ", addr)

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
        print('程序被手动停止')
        break

serversocket.close()
```

自动化交互：  
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