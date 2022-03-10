date='$$$000001&潘宇恒.exe&d:/abcd'
a=8
typenum=1
date1=date[3:9]
while a <= len(date) - 1:
    if date[a]=="&":
        if typenum==1:
            code1=date[10:a]
        if typenum == 2:
            usernicheng=date[end+1:a]
            uiid = date[a+1:]
            break
        end = a
        typenum=typenum+1
    a=a+1
print(code1)
print(usernicheng)
print(uiid)
print(userid)
