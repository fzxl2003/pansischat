from __future__ import print_function

import threading
import time, os
import tkinter

import tkinter.ttk
import requests
import tkinter as tk



import ctypes, sys

def progressbar(url, path):
    """ 带进度条的下载函数 """
    nowsituation=1
    start = time.time()  # 下载开始时间
    response = requests.get(url, stream=True)  # stream=True必须写上
    size = 0  # 初始化已下载大小
    chunk_size = 1024  # 每次下载的数据大小
    content_size = int(response.headers['content-length'])  # 下载文件总大小
    size2 = round(content_size / 1024 / 1024, 2)

    if (size2 < 2):
        updatefail()
        return
    try:
        if response.status_code == 200:  # 判断是否响应成功
            print('Start download,[File size]:{size:.2f} MB'.format(
                size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小
            filepath = path

            with open(filepath, 'wb') as file:  # 显示进度条
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    baifenbi = float(size / content_size * 100)
                    baifenbi = round(baifenbi, 0)
                    a = '\r' + '[下载进度]:' + str(baifenbi) + '%'
                    a = a + '  更新大小：' + str(size2) + 'MB'
                    b = int(size * 50 / content_size)

                    progressbarOne['value'] = b * 2
                    situationlabel.config(text=a)
                    window.update()
                    # print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(size*50/ content_size), float(size / content_size * 100)) ,end=' ')
        end = time.time()  # 下载结束时间
        print('Download completed!,times: %.2f秒' % (end - start))  # 输出下载用时时间
    except:
        updatefail()
    else:

        updatesucccess()


def updatefail():
    progressbarOne['value'] = 0
    situationlabel.config(text='更新失败，请检查网络或联系服务器管理员')
    againlabel.place(x=250, y=150)
    window.update()


def mymovefile(srcfile, dstpath):  # 移动函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        # 移动文件
        print("move %s -> %s" % (srcfile, dstpath + fname))


def openfile(location, f):
    b = os.path.join(location)
    # print("qwds11" + b)
    os.startfile(location)




def updatesucccess():
    global nowsituation
    nowsituation = 2
    situationlabel.config(text='更新成功')


    t1 = threading.Thread(target=ex, args=(url, '组件/main.exe'))
    t1.setDaemon(True)
    t1.start()
    time.sleep(2)
    os._exit(1)

    print('dsadas')
    sys.exit(1)

def ex(a,b):
    print('dsadsadsaas')
    os.startfile("组件\\move.bat")
    sys.exit(1)



def again(event):
    againlabel.place_forget()
    situationlabel.config(text='尝试更新中')

    t1 = threading.Thread(target=progressbar, args=(url, '组件/main.exe'))
    t1.setDaemon(True)
    t1.start()


def windowoff1(event):  ###
    window.destroy()
    sys.exit()


def windowmin1(event):  ###
    window.overrideredirect(False)
    window.iconify()


def windowoff2(event):
    windowoff.config(image=offimage1)


def windowmin2(event):
    windowmin.config(image=minimage1)


def windowoff3(event):
    windowoff.config(image=offimage0)


def windowmin3(event):
    windowmin.config(image=minimage0)


def windowmove(event):
    new_x = (event.x - window.x) + window.winfo_x()
    new_y = (event.y - window.y) + window.winfo_y()
    s = f"{window.winfo_width()}x{window.winfo_height()}+{new_x}+{new_y}"
    window.geometry(s)


def windowclick(event):
    """获取当前窗口位置并保存"""
    window.x, window.y = event.x, event.y


def uizujian():
    global offimage0, offimage1, minimage0, minimage1, progressbarOne, indexbgi, indexlabel, situationlabel, windowmin, windowoff, indexbgimage
    global againlabel
    window.title('更新程序')
    window.geometry('510x258+400+200')
    indexbgimage = tk.PhotoImage(file="组件/ui/2/登录背景3.png")
    indexbgi = tk.Label(window, image=indexbgimage)
    offimage0 = tk.PhotoImage(file="组件/ui/2/关闭0.png")
    minimage0 = tk.PhotoImage(file="组件/ui/2/最小化0.png")
    offimage1 = tk.PhotoImage(file="组件/ui/2/关闭1.png")
    minimage1 = tk.PhotoImage(file="组件/ui/2/最小化1.png")

    indexbgi.config(bg='white')
    indexbgi.place(x=-5, y=-5)
    indexbgi.config(image=indexbgimage)
    indexlabel = tk.Label(window, width=12, font=('宋体', 20, 'bold'), height=1, bg='white', bd=0, text='新版本更新')
    situationlabel = tk.Label(window, width=30, height=2, bg='white', bd=0, text='正在检查更新')
    windowoff = tk.Label(window, image=offimage0, bg='white')
    windowmin = tk.Label(window, image=minimage0, bg='white')
    progressbarOne = tkinter.ttk.Progressbar(window, length=200, mode="determinate")
    # progressbarOne.pack(side=tkinter.TOP)
    againlabel = tk.Label(window, bg='white', text='重试')
    # 进度值最大值
    progressbarOne['maximum'] = 100
    # 进度值初始值
    progressbarOne['value'] = 0
    # progressbarOne.pack()
    window.attributes("-alpha", 0.85)
    windowoff.place(x=465, y=2)
    progressbarOne.place(x=250, y=105)
    windowmin.place(x=435, y=2)
    indexlabel.place(x=15, y=30)
    situationlabel.place(x=250, y=130)
    windowoff.bind("<Enter>", windowoff2)
    windowoff.bind("<Leave>", windowoff3)
    windowmin.bind("<Enter>", windowmin2)
    windowmin.bind("<Leave>", windowmin3)
    indexbgi.bind("<B1-Motion>", windowmove)
    indexbgi.bind("<Button-1>", windowclick)
    againlabel.bind("<Button-1>", again)
    windowmin.bind("<Button-1>", windowmin1)
    windowoff.bind("<Button-1>", windowoff1)
nowsituation=0

def main():
    global window, url,nowsituation


    window = tk.Toplevel()
    window.overrideredirect(True)
    nowsituation=1

    fileurl = open('组件/url.txt', mode='r')
    url = fileurl.read()

    fileurl.close()
    print(url)
    uizujian()
    t1 = threading.Thread(target=progressbar, args=(url, '组件/main.exe'))
    t1.start()
