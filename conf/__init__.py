from threading import Thread,Lock
from time import sleep,ctime


path = r"C:\Users\Administrator\Desktop\serial_streamid.txt"
base_id = 33011701001310001229
def upload_data(filepath,base_id,n=100):
    #准备serial,streamid测试数据方法
    serial_id = base_id
    with open(filepath,'w+',encoding="utf-8") as fp:
        for i in range(n):
            serial_id = str(serial_id+i)
            fp.write(serial_id+','+serial_id+'_MAIN\n')
            fp.flush()
            serial_id = base_id
    
    # filepath = r"C:\Users\Administrator\Desktop\serial_streamid.txt"
    # base_id = 33011701001310000001
    # with open(filepath,'r+') as fp:
    #     s = fp.readlines()
    #     fp.seek(0,0)
    #     for i in s:
    #         fp.write(i.replace(i,i.strip('\n')+','+i.strip('\n')+'_MAIN\n'))
    #         fp.flush()

if __name__ == "__main__":
    upload_data(path, base_id)
    # class test(int):
    #     def __init__(self,value,name):
    #         super().__init__()
    #         print("ending...",name)
            
    #     def __new__(cls,value,name):
    #         print("start...")
    #         return super().__new__(cls,abs(value))
        
    #     def add(self,value):
    #         return value
        
    # i = test(-3,"wangjian")
    # print(i)