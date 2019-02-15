#coding:utf-8
import socket
import sys
'''
创建 socket 对象
AF_INET指定使用IPv4协议，如果要用更先进的IPv6，就指定为AF_INET
SOCK_STREAM指定使用面向流的TCP协议
SOCK_DGRAM指定了这个Socket的类型是UDP
'''
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 获取本地主机名 
host = socket.gethostname() 
# 设置端口号
port = 9999
'''
连接服务，指定主机和端口
80端口是Web服务的标准端口
SMTP服务是25端口
FTP服务是21端口
端口号小于1024的是Internet标准服务的端口，
端口号大于1024的，可以任意使用
'''

for data in [b'g1',b'g2',b'g3']:
    s.sendto(data,(host, port))
    print(s.recv(1024).decode('utf-8'))
s.close()
