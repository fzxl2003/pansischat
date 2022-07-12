import time,os
import requests

def progressbar(url,path):
    """ 带进度条的下载函数 """
    start = time.time() #下载开始时间
    response = requests.get(url, stream=True) #stream=True必须写上
    size = 0    #初始化已下载大小
    chunk_size = 1024  # 每次下载的数据大小
    content_size = int(response.headers['content-length'])  # 下载文件总大小
    try:
        if response.status_code == 200:   #判断是否响应成功
            print('Start download,[File size]:{size:.2f} MB'.format(size = content_size / chunk_size /1024))   #开始下载，显示下载文件大小
            filepath = path
            with open(filepath,'wb') as file:   #显示进度条
                for data in response.iter_content(chunk_size = chunk_size):
                    file.write(data)
                    size +=len(data)
                    print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(size*50/ content_size), float(size / content_size * 100)) ,end=' ')
        end = time.time()   #下载结束时间
        print('Download completed!,times: %.2f秒' % (end - start))  #输出下载用时时间
    except:
        print("Exception occurs in Downloading...")




progressbar('https://12c622023e58e66a1062c803007b0e7f.rdt.tfogc.com:49156/dldir1.qq.com/weixin/Windows/WeChatSetup.exe?mkey=62cd6d4eb9dafb8dc236aefc593b1f9a&arrive_key=25005879836&cip=112.8.56.170&proto=https','wechat.exe')