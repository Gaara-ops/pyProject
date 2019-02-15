#coding:utf-8

import socket
import sys
import threading
import time

def tcplink(sock,addr):
    print('Accept new connection from%s:%s..' % addr)
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') =='exit':
            break
        sock.send(('Hello,%s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print("connect from %s:%s closed." % addr)

#创建 socket 对象
serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
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
#设置最大连接数，超过后排队
#传入的参数指定等待连接的最大数量
serversocket.listen(5)
'''
服务器程序通过一个永久循环来接受来自客户端的连接，
accept()会等待并返回一个客户端的连接
'''
while True:
    #接受一个新连接
    clientsocket,addr = serversocket.accept()
    print("add:%s" % str(addr))
    t = threading.Thread(target=tcplink,args=(clientsocket,addr))
    t.start()
