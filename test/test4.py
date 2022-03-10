import tkinter as tk
from PIL import Image, ImageTk
paned=tk.Tk()
img = Image.open('D:\我的空间\OneDrive\桌面\搜狗截图20210821071345.png')
photo = ImageTk.PhotoImage(img)
tk.Label(paned, image=photo).grid(row=0, column=0)

paned.mainloop()