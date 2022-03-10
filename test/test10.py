import os

date="D:/我的空间/桌面/server.xlsx"
i = 1
while i <= len(date)-1:
    if date[len(date)-i]=="/":
        date=date[:len(date)-i]
    i = i + 1

print(date)

