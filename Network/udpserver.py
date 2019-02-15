#coding:utf-8

import socket
import sys
import threading
import time

#创建 socket 对象
serversocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#获取本地主机名
host = socket.gethostname()
port = 9999
'''
绑定端口号
可以用0.0.0.0绑定到所有的网络地址，还可以用127.0.0.1绑定到本机地址
127.0.0.1是一个特殊的IP地址，表示本机地址，
如果绑定到这个地址，客户端必须同时在本机运行才能连接
'''
serversocket.bind((host,port))
print('bind udp on 9999')
'''
服务器程序通过一个永久循环来接受来自客户端的连接，
accept()会等待并返回一个客户端的连接
'''
while True:
    #接收数据,recvfrom()方法返回数据和客户端的地址与端口
    data ,addr = serversocket.recvfrom(1024)
    print('Received from %s:%s' % addr)
    serversocket.sendto(b'Hello, %s' % data,addr)
