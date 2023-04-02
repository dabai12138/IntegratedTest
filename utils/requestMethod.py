# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import os,sys
import json
from utils.act_file import ActFile,ReadExcel
from utils.remote_operation import RemoteOperation

class BaseRequest(object):
    def __init__(self):
        pass

    def set_url(self,host,port,path):
        port  = port if type(port)==str else str(port)
        path  = path if path.startswith("/") else "/"+path
        self.url = "http://"+host+":"+port+path
        return self.url

    def set_header(self,args):
        header = {"Content-Type":"application/json","Connection":"close"}
        if args:
            header.update(args)
        return header

    def set_params(self,params):
        params = eval(params)
        return params

    def set_data(self,data):
        return data
    
        
class MethodRequest(BaseRequest):
    def __init__(self):
        super(MethodRequest,self).__init__()
        requests.adapters.DEFAULT_RETRIES = 5
        self.s = requests.session()
        self.s.keep_alive = False        

    def GET(self,host,port,api,params,args=None):
        try:
            r = self.s.get(url=self.set_url(host,port,api),params=self.set_params(params),headers=self.set_header(args),timeout=40) if params else requests.get(url=self.set_url(host,port,api),headers=self.set_header(args),timeout=40)
            return r.text
        except Exception as e:
            return str(e)

    def DELETE(self,host,port,api,params,args=None):
        try:
            r = self.s.delete(url=self.set_url(host,port,api),params=self.set_params(params),headers=self.set_header(args),timeout=40) if params else requests.delete(url=self.set_url(host,port,api),headers=self.set_header(args),timeout=40)
            return r.text
        except Exception as e:
            return str(e)

    def POST(self,host,port,api,data,args=None):
        try:
            r = self.s.post(url=self.set_url(host,port,api),data=self.set_data(data),headers=self.set_header(args),timeout=40)
            return r.text
        except Exception as e:
            return str(e)

    def PUT(self,host,port,api,data,args=None):
        try:
            r = self.s.put(url=self.set_url(host,port,api),data=self.set_data(data),headers=self.set_header(args),timeout=40)
            return r.text
        except Exception as e:
            return str(e)
            

if __name__ == "__main__":
    data = '{"serial":"34020000001320000033","keepalive":"True"}'

    ro = MethodRequest()
    ret = ro.POST('192.168.2.184',8080,'/api/v1/stream/start',data=data)
    print(ret)
    