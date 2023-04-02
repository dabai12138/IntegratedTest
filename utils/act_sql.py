# -*- coding: utf-8 -*-

import pymysql
import redis

class ActMysql(object):
    def __init__(self,host,user,passwd,db='vms',port=3306):
        self.conn = pymysql.connect(host,user,passwd,db,port,charset='utf8')
    
    def insertData(self,sql):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            self.cursor.close()
    
    def deleteData(self,sql):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            self.cursor.close()
    
    def updateData(self,sql):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            self.cursor.close()
    
    def queryData(self,sql):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
        except Exception as e:
            print(e)
            data = "query data failed!"
        finally:
            self.cursor.close()
            return data
    
    def closeDB(self):
        self.conn.close()
        print('close mysql successed!')

class ActRedis(object):
    def __init__(self,host,passwd,port):
        pool = redis.ConnectionPool(host=host,port=port,password=passwd)
        self.rd = redis.Redis(connection_pool=pool,decode_responses=True)
  
    def get_str(self,key):
        data = self.rd.get(key)
        return data
    
    def getall_hash(self,name):
        data = self.rd.hgetall(name)
        return data
    
    def get_hash(self,name,key):
        data = self.rd.hget(name,key)
        return data
    
    def get_key(self,keyword=False):
        '''keyword:"*INFO*"'''
        key = self.rd.keys(keyword) if keyword else self.rd.keys()
        return key

if __name__ == "__main__":
    am = ActRedis('192.168.2.184','abc123',6379)
    data = am.get_hash('STREAM:INFO:34020000001320000033_MAIN','publishAddr')
    print(data)
    # k = am.get_key('*INFO*')
    # for s in k:
    #     data = am.get_hash(s.decode(),'status').decode()
    #     print(int(data)==4)