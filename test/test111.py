data=input()
begin=0
data=data[begin+2:-1]
begin=0
newdata=b''
strlen=len(data)
i=1
while (i<strlen):
                    #print(data[i])
                    if (data[i]=='\\'):
                        newdata=newdata+b'\n'+bytes(data[begin+1:i-1],encoding='utf-8')
                        begin=i+1
                    i=i+1
newdata=newdata[1:]+b'\n'
print('hewd')
print(newdata)