
from PIL import Image, ImageTk
import tkinter as tk

from windnd import windnd

sbgwindow=tk.Tk()
sbgwindow.overrideredirect(True)
sbgwindow.title('背景裁切')
sbgwindow.geometry('300x264+400+200')
showwindow = tk.Toplevel()
showwindow.overrideredirect(True)
showwindow.title('标签栏')
showwindow.geometry('300x35+400+165')








def dragged_files(files):
    global image1
    global label1
    global pilimage
    global tkimage
    global msg
    global rewidth
    global reheight
    global bigclick
    global new_x
    global new_y
    global uimain
    bigclick=0
    new_x=0
    new_y=0
    uimain=1

    msg = '\n'.join((item.decode('gbk') for item in files))
    print(msg)
    if msg[-3:]=='png' or msg[-3:]=='jpg':
  #      img = Image.open('D:\我的空间\OneDrive\桌面\搜狗截图20210821071345.png')
 #       photo = ImageTk.PhotoImage(img)
#        tk.Label(paned, image=photo).grid(row=0, column=0)

        pilimage = Image.open(msg)
        tkimage = ImageTk.PhotoImage(image=pilimage)
        label1=tk.Label(sbgwindow,image=tkimage)
        (rewidth,reheight)=pilimage.size
        label1.place(x=0, y=0)
        bigbutton.place(x=50,y=10)
        smallbutton.place(x=70, y=10)
        baocunbutton.place(x=110,y=10)
        uimainbutton.place(x=90,y=10)
        yulanbutton.place(x=150,y=10)
        def label1move(event):
            global new_x
            global new_y

            new_x = (event.x - label1.x) + label1.winfo_x()
            new_y = (event.y - label1.y) + label1.winfo_y()
            label1.place(x=new_x, y=new_y)
            print('x='+ str(new_x))
            print('y=' + str(new_y))


        def label1click(event):
            """获取当前窗口位置并保存"""
            label1.x, label1.y = event.x, event.y
        def baocun(event):
            global new_x
            global new_y
            baocunimg= pilimage.crop((new_x*-1, new_y*-1,new_x*-1+300,new_y*-1+264))  # (left, upper, right, lower)

            img1=Image.open('组件\\ui\\新增ui\\'+str(uimain)+'表头.png')
            size1, size2 = img1.size, baocunimg.size
            joint = Image.new('RGB', (size1[0], size1[1] + size2[1]))
            loc1, loc2 = (0, 0), (0, size1[1])
            joint.paste(img1, loc1)
            joint.paste(baocunimg, loc2)
            joint.save('vertical.png')



        label1.bind("<B1-Motion>", label1move)
        label1.bind("<Button-1>", label1click)
        sbgwindow.bind('<MouseWheel>', mousemove)


        label1.bind("<Double-Button-1>",baocun)


def windowmove(event):
    wnew_x = (event.x - showwindow.x) + showwindow.winfo_x()
    wnew_y = (event.y - showwindow.y) + showwindow.winfo_y()
    s = f"{showwindow.winfo_width()}x{showwindow.winfo_height()}+{wnew_x}+{wnew_y}"
    w=f"{sbgwindow.winfo_width()}x{sbgwindow.winfo_height()}+{wnew_x}+{wnew_y+35}"
    showwindow.geometry(s)
    sbgwindow.geometry(w)

def windowclick(event):
        """获取当前窗口位置并保存"""
        showwindow.x, showwindow.y = event.x, event.y

def baocun():
    global new_x
    global new_y
    baocunimg = pilimage.crop(
        (new_x * -1, new_y * -1, new_x * -1 + 300, new_y * -1 + 264))  # (left, upper, right, lower)

    img1 = Image.open('组件\\ui\\新增ui\\' + str(uimain) + '表头.png')
    size1, size2 = img1.size, baocunimg.size
    joint = Image.new('RGB', (size1[0], size1[1] + size2[1]))
    loc1, loc2 = (0, 0), (0, size1[1])
    joint.paste(img1, loc1)
    joint.paste(baocunimg, loc2)
    joint.save('vertical.png')

def bigger():
    global pilimage
    global tkimage
    global nowwidth
    global nowheight
    global bigclick
    (imgwidth, imgheight) = pilimage.size
    bigclick = bigclick + 1
    if bigclick > 2 and rewidth > imgwidth:
        pilimage = Image.open(msg)
        tkimage = ImageTk.PhotoImage(image=pilimage)
        bigclick = 0

    imgwidth = int(float(imgwidth) * 1.2)
    imgheight = int(float(imgheight) * 1.2)
    pilimage = pilimage.resize((imgwidth, imgheight))

    tkimage = ImageTk.PhotoImage(image=pilimage)
    label1.config(image=tkimage)
def smaller():
    global pilimage
    global tkimage
    global nowwidth
    global nowheight
    global bigclick
    bigclick = 0
    (imgwidth, imgheight) = pilimage.size
    imgwidth = int(float(imgwidth) * 0.8)
    imgheight = int(float(imgheight) * 0.8)
    pilimage = pilimage.resize((imgwidth, imgheight))
    print(pilimage.size)
    tkimage = ImageTk.PhotoImage(image=pilimage)
    label1.config(image=tkimage)
def ui():
    global uimain
    if uimain==1:
        uimainbutton.config(bg='black')
    if uimain==2:
        uimainbutton.config(bg='white')

def chooseuimain():
    global uimain
    uiwindow = tk.Toplevel()
    uiwindow.overrideredirect(True)
    uiwindow.title('标签栏')
    x=showwindow.winfo_x()+50
    y=showwindow.winfo_y()+10
    chooseuilocate= f"70x70+{x}+{y}"
    uiwindow.geometry(chooseuilocate)
    def uiblack():
        global uimain
        uimain=1
        uiwindow.destroy()
        ui()
    def uiwhite():
        global uimain
        uimain=2
        uiwindow.destroy()
        ui()

    blackbutton=tk.Button(uiwindow,bg='black',command=uiblack,height=1,width=3)
    whitebutton=tk.Button(uiwindow,bg='white',command=uiwhite,height=1,width=3)
    blackbutton.pack()
    whitebutton.pack()

def yulan():
    global new_x
    global new_y
    global joint
    global joint1
    baocunimg = pilimage.crop(
        (new_x * -1, new_y * -1, new_x * -1 + 300, new_y * -1 + 264))  # (left, upper, right, lower)
    img1 = Image.open('组件\\ui\\新增ui\\' + str(uimain) + '表头.png')
    size1, size2 = img1.size, baocunimg.size
    joint = Image.new('RGB', (size1[0], size1[1] + size2[1]))
    loc1, loc2 = (0, 0), (0, size1[1])
    joint.paste(img1, loc1)
    joint.paste(baocunimg, loc2)
    yulanwindow = tk.Toplevel()
    joint1 = ImageTk.PhotoImage(image=joint)
    yulanlabel=tk.Label(yulanwindow,image=joint1)

    yulanlabel.pack()



  #  yulanwindow.overrideredirect(True)
   # yulanwindow.title('标签栏')
    #yulanwindow.geometry('800x530+400+200')
    #baocunimg = pilimage.crop((new_x * -1, new_y * -1, new_x * -1 + 300, new_y * -1 + 258))  # (left, upper, right, lower)



def mousemove(event):
    global pilimage
    global tkimage
    global nowwidth
    global nowheight
    global bigclick
    if event.delta > 1:
        (imgwidth, imgheight) = pilimage.size
        bigclick = bigclick + 1
        if bigclick > 2 and rewidth > imgwidth:
            pilimage = Image.open(msg)
            tkimage = ImageTk.PhotoImage(image=pilimage)
            bigclick = 0

        imgwidth = int(float(imgwidth) * 1.2)
        imgheight = int(float(imgheight) * 1.2)
        pilimage = pilimage.resize((imgwidth, imgheight))

        tkimage = ImageTk.PhotoImage(image=pilimage)
        label1.config(image=tkimage)
    if event.delta < 1:
        bigclick = 0
        (imgwidth, imgheight) = pilimage.size
        imgwidth = int(float(imgwidth) * 0.8)
        imgheight = int(float(imgheight) * 0.8)
        pilimage = pilimage.resize((imgwidth, imgheight))
        print(pilimage.size)
        tkimage = ImageTk.PhotoImage(image=pilimage)
        label1.config(image=tkimage)

showlabeltitle=tk.Label(showwindow,text='图片截取')
bigbutton=tk.Button(showwindow,text='+',command=bigger)
smallbutton=tk.Button(showwindow,text='-',command=smaller)
uimainbutton=tk.Button(showwindow,bg='black',command=chooseuimain)
yulanbutton=tk.Button(showwindow,text='预览',command=yulan)
baocunbutton=tk.Button(showwindow,text='保存',command=baocun)
showlabeltitle.place(x=0,y=0)

showwindow.bind("<B1-Motion>", windowmove)
showwindow.bind("<Button-1>", windowclick)









windnd.hook_dropfiles(sbgwindow,func=dragged_files)






sbgwindow.mainloop()