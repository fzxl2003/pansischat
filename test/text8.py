# coding=utf-8
# This is a sample Python script.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import tkinter as tk
from tkinter import FLAT
from socket import *
import time
import os
from cryptography.fernet import Fernet
from openpyxl import Workbook
from openpyxl import load_workbook
import random                 #引用区
from threading import Thread
import fileserver
logcode=b'w2V8gAUFER-9uq6lKG7AfpYI6AcINEs7Ipm4KyQj2AI='  #登录密码秘钥
global userwithip


on=1


userwithip={}   #ip与登录的用户的字典查询

def encrypt1(date,cipher_key):     # 进行加密

    date = bytes(date, encoding='utf-8')

    encrypted_text = Fernet(cipher_key).encrypt(date)

    encrypted_text = str(encrypted_text, encoding='utf-8')
    return encrypted_text


def decrypt1(date, cipher_key):  # 进行解密
    if date[:2] == 'b\'':
        print('123')
        date = date[2:]
        date = date[:-1]
        print(date)
    date = bytes(date, encoding='utf-8')
    print(date)
    print(cipher_key)
    decrypted_text = '1234'
    try:
        decrypted_text = Fernet(cipher_key).decrypt(date)
        decrypted_text = str(decrypted_text, encoding='utf-8')
    except:

        print(decrypted_text)
    return decrypted_text









global threadnum
threadnum=0
a=''

def fileserve(a,port):
    fileserver.start(port)
def ser0020():
    a=1
    port=random.randint(10000,50000)
    fileserve1 = Thread(target=fileserve, args=(a,port))
    fileserve1.start()
    return port


def readmsg(clientsocket,clientinfo):
 global threadnum


 #print('ok')
 print(clientinfo)
 while True:
     try:
         receivedate = clientsocket.recv(1024)  # 等待接受(数据最大为1024)
         print(receivedate)
     except:
         clientsocket.close()
         threadnum = threadnum - 1
         print("一线程关闭")
         break
     else:
         nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 格式化成2016-03-20 11:45:39形式
         print(receivedate.decode('gb2312'))
         receivedate=receivedate.decode('gb2312')
         # print('来自%s<%s> \n %s' % (receivedate[1], nowtime, receivedate[0].decode('gb2312')))
         指令 = receivedate[0:4]
         ip = clientinfo
         #print(ip)
         if 指令 == '0020':

             port=ser0020()
             a="0021"+ str(port)
             clientsocket.send(a.encode('gb2312'))








def main():
    global udps
    global userwithip
    global threadnum
    udps = socket(AF_INET, SOCK_STREAM)  # 创建套接字
    udps.bind(('', 8080))  # 本机软件绑定端口
    while True:
      udps.listen()  # 监听连接并等待




      clientsocket,clientinfo = udps.accept()  # 接收连接后获取客户端信息
                                           # 开启线程处理当前客户端请求
      t = Thread(target=readmsg, args=(clientsocket, clientinfo))

      t.start()
      threadnum=threadnum+1
    #  t2 = Thread(target=sendnewmessgae, args=(clientsocket, clientinfo))
     # threadnum = threadnum + 1

     # t2.start()
      print("开启的线程数：" + str(threadnum))






main()






