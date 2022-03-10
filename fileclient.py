import sys



sys.path.append("..")
from Helper.LFTPMessage import LFTPMessage
from Helper.LFTPRecvWindow import LFTPRecvWindow
from Helper.LFTPSendWindow import LFTPSendWindow
from Utils.Log import *


from socket import *
import json
import os
import time
import struct
from progressbar import *
import threading
import random

from enum import Enum
global pbar

global filesituation
global filesituationtxt


# 表示客户端的状态
class State(Enum):
    CLOSED = 0
    SYN_SEND = 1
    ESTABLISHED = 2   #连接成功
    CLOSN_WAIT = 3
    LAST_ACK = 4 

class LFTPClient:
    global filesituation

    global filesituationtxt
    global uploadfilesituation,uploadfilesituationtxt

    def __init__(self, host, port, bufferSize):
        global filesituation
        self.host = host
        self.port = port
        self.bufferSize = bufferSize
        self.udpClient = socket(AF_INET,SOCK_DGRAM)
        self.state = State.CLOSED
        filesituation = 0
        self.lock = threading.Lock()
        # 用于三次握手
        self.server_isn = -1
        self.client_isn = random.randint(0, 1000)
        # cwnd
        self.cwnd = 1
        self.rwnd = 1000
        self.ssthresh = 8
        # 定时器
        self.timer = None
        self.TimeoutInterval = 0.01

    # 仅提供一次性服务
    def start(self, LFTPType, filename,nowfilelocation):
        if LFTPType == "UPLOAD":
            self.ControlHandShake()
            self.UpLoadFile(nowfilelocation)
        elif LFTPType == "DOWNLOAD":
            self.ControlHandShake()
            self.DownloadFile(filename,nowfilelocation)
        else:
            print(">>> 输入传输类型错误")

    def ControlHandShake(self):
        global filesituation

        global filesituationtxt,uploadfilesituation,uploadfilesituationtxt
        con_time = 0
        self.udpClient.settimeout(2)
        #self.udpClient.sendto(b'request.pack()', (self.host, port))
        while True:
            # 发送请求获取分配端口
            request = LFTPMessage(getport=1)
            request.getport = 1
            self.udpClient.sendto(request.pack(), (self.host, self.port))
            try:
                message = self.udpClient.recv(2048)
            except Exception as e:
                con_time += 1
                if con_time == 10:
                    log_error("连接失败，网络/服务端故障")
                    filesituationtxt="下载失败，网络/服务端故障"
                    filesituation=0
                    uploadfilesituationtxt = "上传失败，网络/服务端故障"
                    uploadfilesituation = 0

                  #  main.result.delete(str(main.filelistline[filename1]) + '.0',str(main.filelistline[filename1]) + '.end')
                  #  main.result.insert(str(main.filelistline[filename1]) + '.0', filename1 + "  正在下载  连接失败，网络/服务端故障")
                    return False
                log_warn("连接超时, 重新连接中, 连接次数： ", con_time)
                filesituationtxt = "连接超时, 重新连接中, 连接次数： "+str(con_time)
                uploadfilesituationtxt = "连接超时, 重新连接中, 连接次数： " + str(con_time)
                continue
            message = LFTPMessage.unpack(message)
            if message.getport == 1:
                data = json.loads(message.content[:message.content_size].decode("utf-8"))
                self.port = data["port"]
                #a=b'123456'
                #message = LFTPMessage(SYN=1, seqnum=self.client_isn, content_size=len(a),content=a)
                #self.udpClient.sendto(message.pack(), (self.host, self.port))
                #a=b'123'
                return True

    def handshake(self, LFTPType, filename, filesize = 0):
        global filesituation
        global filesituationtxt,uploadfilesituation,uploadfilesituationtxt,uploadport
        log_info("开始连接服务器")
        filesituationtxt ="开始连接服务器"
        uploadfilesituationtxt = "开始连接服务器"
        # main.result.delete(str(main.filelistline[filename1]) + '.0', str(main.filelistline[filename1]) + '.end')
        #main.result.insert(str(main.filelistline[filename1]) + '.0', filename1 + "  正在下载  开始连接服务器")
        i=0
        while i<=len(filename)-1:
            if filename[i]=='/':
                filename=filename[i+1:]

                break
            i=i+1
        print("文件名："+filename)
        self.fileInfo = {
            "filename": filename,
            "filesize": filesize,
            "LFTPType": LFTPType
        }
        fileInfojson = json.dumps(self.fileInfo).encode("utf-8")
        message = LFTPMessage(SYN=1, seqnum=self.client_isn, content_size=len(fileInfojson), content=fileInfojson)

        self.udpClient.sendto(message.pack(), (self.host, self.port))

        self.state = State.SYN_SEND
        threading.Timer(0.2, self.handshakeTimer, [self.state, message, 0]).start()
        log_info("发送第一次握手报文")

        while True:
            try:
                res = self.udpClient.recv(2048)
            except Exception as e:
                log_warn("接收回应报文超时")
                if self.state == State.CLOSED:
                    filesituationtxt = "下载失败：连接服务器失败"
                    filesituation = 0
                    uploadfilesituationtxt = "上传失败：连接服务器失败"
                    uploadfilesituation = 0
                    log_error("连接失败")
                    #   main.result.delete(str(main.filelistline[filename1]) + '.0',
                                       #str(main.filelistline[filename1]) + '.end')
                    #   main.result.insert(str(main.filelistline[filename1]) + '.0', filename1 + "  正在下载  连接失败")
                    break
                continue
            res = LFTPMessage.unpack(res)
            if self.state == State.SYN_SEND and res.SYN == 1 and res.ACK == 1 and res.acknum == self.client_isn+1:
                log_info("收到第二次握手响应报文")
                if self.fileInfo["LFTPType"] == "DOWNLOAD":
                    self.fileInfo = json.loads(res.content[:res.content_size].decode("utf-8"))
                    if self.fileInfo["filesize"] == -1:
                        log_error("文件不存在，无法提供下载：", self.fileInfo["filename"])
                        filesituationtxt = "下载失败：文件不存在或过期"
                        #  main.result.delete(str(main.filelistline[filename1]) + '.0',
                        #                   str(main.filelistline[filename1]) + '.end')
                        #  main.result.insert(str(main.filelistline[filename1]) + '.0', filename1 + "  正在下载  文件不存在，无法提供下载")
                        self.state = State.CLOSED
                        filesituation = 0
                        return
                self.server_isn = res.seqnum
                reply_message = LFTPMessage(SYN=0, ACK=1, seqnum=self.client_isn+1, acknum=self.server_isn+1)
                self.udpClient.sendto(reply_message.pack(), (self.host, self.port))
                self.state = State.ESTABLISHED
                log_info("发送第三次握手报文")
                log_info("连接建立完毕")
                filesituationtxt ="连接服务器成功"
                uploadfilesituationtxt = "连接服务器成功"
                uploadport = str(self.port)
                break

    def handshakeTimer(self, state, message, timeout):
        global filesituation,uploadfilesituation,uploadfilesituationtxt

        global filesituationtxt,uploadport
        if (state == self.state):
            if timeout == 10:
                log_error("第一次握手失败")
                self.state = State.CLOSED
                filesituationtxt ="下载失败"
                filesituation = 0
                uploadfilesituationtxt = "上传失败"
                uploadfilesituation = 0
                return
            if (state == State.SYN_SEND):
                self.udpClient.sendto(message.pack(), (self.host, self.port))
                threading.Timer(0.2, self.handshakeTimer, [self.state, message, timeout+1]).start()
                log_warn("第一次握手超时，重新发送第一次握手报文, 当前超时次数：", timeout+1)
                log_warn('连接端口为：'+str(self.port))

                filesituationtxt ="下载出现问题，尝试连接中"
                uploadfilesituationtxt = "上传出现问题，尝试连接中"



    def UpLoadFile(self, filepath):
        global filesituation

        global filesituationtxt,uploadfilesituation,uploadfilesituationtxt
        try:
            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath)
        except Exception as e:
            log_error("文件不存在或打开错误:", filepath)
            uploadfilesituationtxt = "上传失败，文件不存在或打开错误:"+filepath
            uploadfilesituation = 0
            return
        # 发起握手建立连接
        self.handshake("UPLOAD", filename, filesize)
        # 握手完毕未进入连接建立状态，退出
        if self.state != State.ESTABLISHED:
            log_error("连接建立失败，无法上传文件")
            uploadfilesituationtxt = "上传失败，无法连接服务器"
            uploadfilesituation = 0
            self.state = State.CLOSED
            #filesituation = 0
            return

        self.send_window = LFTPSendWindow(0, self.rwnd)

        # 应用端持续读取数据填入发送窗口
        with open(filepath, 'rb') as f:
            log_info("开始传送文件:",filename)
            uploadfilesituationtxt = "开始传送文件:"+filename
            threading.Thread(target=self.recvACK, args=(filesize,)).start()
            uploadfilesituation=1
            while filesize > 0:
                if uploadfilesituation == -2:
                    log_error("用户取消上传")
                    uploadfilesituationtxt = "上传失败：用户取消上传"
                    uploadfilesituation = 0
                    pbar.finish()
                    self.state = State.CLOSED
                    break
                if (self.send_window.isFull()): # 窗口已经满了
                    time.sleep(0.00001)
                    continue
                if filesize >= self.bufferSize:
                    content = f.read(self.bufferSize)  # 每次读出来的文件内容
                    self.lock.acquire()
                    self.send_window.append(content)
                    self.lock.release()
                    filesize -= self.bufferSize
                else:
                    content = f.read(filesize)  # 最后一次读出来的文件内容
                    self.lock.acquire()
                    self.send_window.append(content)
                    self.lock.release()
                    filesize = 0
                    break

    # 接收客户端ACK，滑动窗口
    def recvACK(self, filesize):
        # pbar = ProgressBar().start()
        global uploadfilesituation,uploadfilesituationtxt

        # 发送第一个数据报文，此时cwnd = 1
        self.cwnd = 1
        while True:
            self.lock.acquire()
            if self.send_window.isEmpty() == False:
                item = self.send_window.getItemToSend()
                if item != None:
                    self.lock.release()
                    break
            self.lock.release()

        first_message = LFTPMessage(seqnum=item.seqnum, content_size=len(item.content), content=item.content)
        self.udpClient.sendto(first_message.pack(), (self.host, self.port))
        # 设置超时定时器
        self.timer = threading.Timer(self.TimeoutInterval, self.TimeOutAndReSend)
        self.timer.start()

        self.origin_time = time.time()
        self.last_time = time.time()
        self.last_recvsize = 0
        self.compute_result = 0
        self.total_result = 0

        recvSize = 0
        while(True):
            # 接收信息
            try:
                message = self.udpClient.recv(2048)
            except Exception as e:
                if filesize == recvSize:
                    pbar.finish()
                    log_info("服务端接收完毕")
                    uploadfilesituationtxt = "上传完成"
                    uploadfilesituation = -1
                    self.timer.cancel()
                else:
                    log_error("超时重连失败")
                    uploadfilesituationtxt = "上传失败，无法连接服务器"
                    uploadfilesituation = 0
                    self.timer.cancel()
                break
            message = LFTPMessage.unpack(message)
            acknum = message.acknum

            self.lock.acquire()
            # 更新滑动窗口
            if self.cwnd < self.ssthresh:
                self.cwnd += 1
            else:
                self.cwnd += 1/int(self.cwnd)
            # 更新rwnd
            self.send_window.ACKseqnum(acknum)
            self.rwnd = message.rwnd
            self.send_window.rwnd = message.rwnd
            # log_info("rwnd: ", self.rwnd, ", cwnd: ", self.cwnd)
            #  # 确认一波
            # log_info(acknum, " ACKTIME: ",self.send_window.getACKTimeBySeqnum(acknum))
            if self.send_window.getACKTimeBySeqnum(acknum) == 4:
                # 三次冗余进行重传，同时更新cwnd和ssthresh
                # log_warn("三次冗余", acknum)
                self.ssthresh = self.cwnd/2
                self.cwnd = self.cwnd/2+3
                r_content = self.send_window.getContentBySeqnum(acknum)
                r_message = LFTPMessage(seqnum=acknum, content_size=len(r_content), content=r_content)
                self.udpClient.sendto(r_message.pack(), (self.host, self.port))
                # 重新设置超时定时器
                self.timer.cancel()
                self.timer = threading.Timer(self.TimeoutInterval, self.TimeOutAndReSend)
                self.timer.start()
            elif self.send_window.getACKTimeBySeqnum(acknum) == 1:
                # 首次接收到，send_base改变
                recvSize += self.send_window.updateSendBase(acknum)
                List = self.send_window.getSendList(self.cwnd)
                for item in List:
                    message = LFTPMessage(seqnum=item.seqnum, content_size=len(item.content), content=item.content)
                    self.udpClient.sendto(message.pack(), (self.host, self.port))
                # 重新设置超时定时器
                self.timer.cancel()
                self.timer = threading.Timer(self.TimeoutInterval, self.TimeOutAndReSend)
                self.timer.start()
            elif self.send_window.getACKTimeBySeqnum(acknum) == -1:
                recvSize = filesize
                self.UpLoadProgress(recvSize, filesize)
                log_info("服务端接收完毕")
                uploadfilesituationtxt = "上传完成"
                uploadfilesituation = -1
                self.timer.cancel()
                self.lock.release()
                break

            self.lock.release()
            self.UpLoadProgress(recvSize, filesize)
            # pbar.update(int(recvSize/filesize)*100)

            if filesize == recvSize:
                pbar.finish()
                log_info("服务端接收完毕")
                uploadfilesituationtxt = "上传完成"
                uploadfilesituation = -1
                self.timer.cancel()
                break
    
    # 显示下载进度函数
    def DownLoadProgress(self, recvSize, filesize):
        global filesituationtxt
        time_change = time.time() - self.last_time
        size_change = recvSize - self.last_recvsize
        if (time_change >= 0.7):
            self.last_time = time.time()
            self.last_recvsize = recvSize
            self.compute_result = size_change/time_change/1024
            self.total_result = recvSize/(time.time()-self.origin_time)/1024
        print('\r%d/%d  已经下载： %d%%  当前下载速度： %d kb/s  平均下载速度： %d kb/s' % \
            (recvSize, filesize, int(recvSize/filesize*100), self.compute_result, self.total_result), end='')
        speed=self.compute_result
        if self.compute_result>1024.00:
            speed=speed / 1000
            speed=round(speed,2)
            speedtxt=str(speed) +"Mb/s"
        else:speedtxt=str(round(speed,2)) +"Kb/s"
        filesituationtxt = "  下载：" +str(int(recvSize/filesize*100))+  "%  速度："+speedtxt
        # main.result.delete(str(main.filelistline[filename1]) + '.0', str(main.filelistline[filename1]) + '.end')
        #main.result.insert(str(main.filelistline[filename1]) + '.0', filename1 + "下载：" +str(int(recvSize/filesize*100))+  "%  速度："+str(self.compute_result)+  "kb/s"  )
        if recvSize == filesize:
            print("")

    # 定时器，超时重传，必定重传的是send_base
    def TimeOutAndReSend(self):
        self.lock.acquire()
        self.ssthresh = self.cwnd/2
        self.cwnd = 1
        seqnum = self.send_window.send_base
        content = self.send_window.getContentBySeqnum(seqnum)
        self.lock.release()
        if content == None:
            return
        # log_warn("超时重传：", seqnum)
        message = LFTPMessage(seqnum=seqnum, content_size=len(content), content=content)
        self.udpClient.sendto(message.pack(), (self.host, self.port))
        self.timer.cancel()
        self.timer = threading.Timer(self.timer.interval*2, self.TimeOutAndReSend)
        self.timer.start()

    def DownloadFile(self, filename,nowfilelocation):
        global filesituation

        global filesituationtxt
        # 发起握手建立连接
        self.handshake("DOWNLOAD", filename)
        # 握手完毕未进入连接建立状态，退出
        if self.state != State.ESTABLISHED:
            log_error("连接建立失败，无法下载文件")
            filesituationtxt="下载失败：无法连接服务器"
            #  main.result.delete(str(main.filelistline[filename1]) + '.0', str(main.filelistline[filename1]) + '.end')
            #  main.result.insert(str(main.filelistline[filename1]) + '.0', filename1 + "  连接建立失败，无法下载文件")
            self.state = State.CLOSED
            filesituation = 0
            return
        filename = self.fileInfo["filename"]
        filesize = self.fileInfo["filesize"]

        self.recv_base = 0  # 当前窗口基序号
        self.N = 1000 # 窗口大小
        self.window = [] # 接收方窗口
        for i in range(self.N):
            self.window.append(None)

        self.origin_time = time.time()
        self.last_time = time.time()
        self.last_recvsize = 0
        self.compute_result = 0
        self.total_result = 0
        recvsize = 0 # 已接收数据大小
        i = 0
        while i <= len(filename) - 1:
            if filename[i] == '/':
                filename = filename[i + 1:]
                break
            i = i + 1
        print("文件名：" + filename)

        log_info("开始接收文件 %s"%(filename))
        filesituationtxt =filename + "  开始下载 "
        #  main.result.delete(str(main.filelistline[filename1]) + '.0', str(main.filelistline[filename1]) + '.end')
        # main.result.insert(str(main.filelistline[filename1]) + '.0', filename1 + "  正在下载 ")
        with open(nowfilelocation+"/"+filename, 'wb') as f:
            # pbar = ProgressBar().start()
            self.udpClient.settimeout(8)                                                                                          #######超时重传时间
            while True:
                if filesituation == -2:
                    log_error("用户取消下载")
                    filesituationtxt = "下载失败：用户取消下载"
                    filesituation = 0
                    self.state = State.CLOSED
                    break
                try:
                    message = self.udpClient.recv(2048)
                except Exception as e:

                    if (recvsize == filesize):
                        # pbar.finish()
                        log_info("接收完毕，断开连接")
                        filesituationtxt ="下载完成"
                        filesituation = -1
                        #             main.result.delete(str(main.filelistline[filename1]) + '.0',
                        #                           str(main.filelistline[filename1]) + '.end')
                        #           main.result.insert(str(main.filelistline[filename1]) + '.0', filename1 + "下载完成")    ############################
                    else:
                        log_error("连接已断开")
                        filesituationtxt = "下载失败：连接已断开"
                        filesituation = 0
                        #   main.result.delete(str(main.filelistline[filename1]) + '.0',
                        #                      str(main.filelistline[filename1]) + '.end')
                        #  main.result.insert(str(main.filelistline[filename1]) + '.0', filename1 + "下载失败")
                    break

                message = LFTPMessage.unpack(message)
                seqnum = message.seqnum
                content = message.content
                content_size = message.content_size
                #a=b'123456'
                #message1 = LFTPMessage(seqnum=seqnum, content_size=len(a), content=a)
                #self.udpClient.sendto(message1.pack(), (self.host, self.port))
                if (seqnum >= self.recv_base and seqnum < self.recv_base + self.N):
                    self.window[seqnum - self.recv_base] = content[:content_size]
                while self.window[0] != None:
                    f.write(self.window[0])
                    recvsize += len(self.window[0])
                    # pbar.update(int(recvsize / filesize * 100))
                    self.DownLoadProgress(recvsize, filesize)
                    self.window.pop(0)
                    self.window.append(None)
                    self.recv_base += 1

                rwnd = 0
                for item in self.window:
                    if item == None:
                        rwnd += 1
                response = LFTPMessage(ACK=1, seqnum=seqnum, rwnd=rwnd, acknum=self.recv_base)

                if (seqnum <= self.recv_base + self.N):
                    self.udpClient.sendto(response.pack(), (self.host, self.port))

    # 显示上传进度函数
    def UpLoadProgress(self, recvSize, filesize):
        global uploadfilesituation, uploadfilesituationtxt
        time_change = time.time() - self.last_time
        size_change = recvSize - self.last_recvsize
        if (time_change >= 0.7):
            self.last_time = time.time()
            self.last_recvsize = recvSize
            self.compute_result = size_change/time_change/1024
            self.total_result = recvSize/(time.time()-self.origin_time)/1024
        print('\r%d/%d  已经上传： %d%%  当前上传速度： %d kb/s  平均上传速度： %d kb/s' % \
            (recvSize, filesize, int(recvSize/filesize*100), self.compute_result, self.total_result), end='')
        speed = self.total_result
        if self.compute_result > 1024.00:
            speed = speed / 1000
            speed = round(speed, 2)
            speedtxt = str(speed) + "Mb/s"
        else:
            speedtxt = str(round(speed, 2)) + "Kb/s"
        uploadfilesituationtxt = "  上传：" + str(int(recvSize / filesize * 100)) + "%  速度：" + speedtxt
        if recvSize == filesize:
            print("")

def getHelp():
    tip = "指令格式：\n" +\
          "  发送文件: LFTP lsend myserver mylargefile\n"+\
          "  下载文件: LFTP lget myserver mylargefile\n"+\
          "参数设置：\n"+\
          "  myserver：url地址或者ip地址\n"+\
          "  mylargefile： 文件路径"
    print('\033[33m%s' % tip)

def download1(filename,nowfilelocation):
    global filename1
    iptxt = open('组件/ip.txt', mode='r')
    IP = iptxt.read()
    iptxt.close()
    filename1=filename
    client = LFTPClient(IP, 12345, 1024)

    client.start("DOWNLOAD", filename,nowfilelocation)
    return
def upload1(filename,nowfilelocation):
    global uploadport
    uploadport = ''
    iptxt = open('组件/ip.txt', mode='r')
    IP = iptxt.read()
    iptxt.close()
    client = LFTPClient(IP, 12345, 1024)
    client.start("UPLOAD", filename,nowfilelocation)

    return




  #   if len(sys.argv) != 5:
 #       getHelp()
 #   else:
  #      if sys.argv[1] != "LFTP":
  #          getHelp
  #      else:
   #         if sys.argv[2] == "lsend":
  #              IP = sys.argv[3]
   #             filename = sys.argv[4]
   #             client = LFTPClient(IP, 12345, 1024)
   #             client.start("UPLOAD", filename)
    #        elif sys.argv[2] == "lget":
    #            IP = sys.argv[3]
     #           filename = sys.argv[4]
     #           client = LFTPClient(IP, 12345, 1024)
      #          client.start("DOWNLOAD", filename)
     #       else:
     #           getHelp()
        
        # client = LFTPClient('127.0.0.1', 12345, 1024)
        # client = LFTPClient('192.168.199.129', 12345, 1024)
#nowfilelocation="D:\\我的空间\\桌面\\"

#print(nowfilelocation)
#date="0020"
#tcps.send(date.encode('gb2312'))
#download1(filename,nowfilelocation)