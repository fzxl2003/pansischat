import tkinter
import windnd
from tkinter.messagebox import  showinfo
def dragged_files(files):
    msg = '\n'.join((item.decode('gbk') for item in files))
    showinfo('您拖放的文件',msg)
tk = tkinter.Tk()
windnd.hook_dropfiles(tk,func=dragged_files)
tk.mainloop()