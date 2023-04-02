#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import time
import re
import json
import pysnooper
from utils import *
from utils.remote_operation import RemoteOperation
from utils.requestMethod import MethodRequest
from utils.get_loginfo import GetLogs
from utils.act_file import ActFile,ReadExcel
from utils.act_conf import ReadConf
from utils.act_sql import ActRedis,ActMysql
from threading import Thread

class RunCase(object):
    def __init__(self,casename):
        self.re = ReadExcel(casename)
        self.af = ActFile()
        self.ro = RemoteOperation()
        self.gl = GetLogs(self.ro)
        self.mr = MethodRequest()
          
    def get_current_time(self):
        time_list = []
        for f in format_time:
            current_time = time.strftime(f,time.localtime(time.time()))
            time_list.append(current_time)
        return time_list

    def get_case_step(self):
        nrows = self.re.get_rows()
        case_list = []
        case_dict = {}
        space_num = 0
        for n in nrows:
            if not n[0]:
                space_num += 1
        if space_num:
            for index,row in enumerate(nrows):     
                if row[0]:
                    case_list.append(row)
                    if len(case_dict) == space_num:
                        case_dict[case_list[0][0]] = nrows[index:]              
                else:
                    case_dict[case_list[0][0]] = case_list
                    case_list = []
        else:
            case_dict[nrows[0][0]] = nrows
        return case_dict


    def get_redis_hash(self,host,passwd,name,port):
        ar = ActRedis(host,passwd,port)
        if ',' not in name:
            value = ar.getall_hash(name)
        else:
            name,key = name.split(',') 
            value = ar.get_hash(name, key)
            value = [value]
        return value
    
    def query_mysql_data(self,host,user,passwd,sql):
        am = ActMysql(host,user,passwd)
        data = am.queryData(sql)
        return data
    #@pysnooper.snoop()
    def get_loginfo(self,current_time,host_list):
        host_list = list(set(host_list))
        s_list = []
        log_list = []
        stdout_list = []
        stdout_dict = {}
        for host in host_list:
            self.gl.ssh_open(host,ssh_user,ssh_passwd)
            for c_time,l_path,f_time,s_name in zip(current_time,logpath_list,format_time,server_list):
                stdout = self.gl.get_loginfo(c_time,l_path,f_time,s_name)
                if stdout:
                    stdout[0] = f'**{host}**:This is {s_name} log content:\r\n'+stdout[0]
                else:
                    stdout = f'**{host}**:This is {s_name} log content:\r\n'
                s_list.append(stdout)
            stdout_dict[host] = s_list
            s_list = []
            self.gl.ssh_close()
        for n in range(len(list(stdout_dict.values())[0])):
            log_list = []
            for std_list in stdout_dict.values():
                log_list+=std_list[n] 
            stdout_list.append(log_list)
        return stdout_list
        
    def write_to_logs(self,current_time,key,cont_list,step_list,return_dict):
        stdout_list = self.get_loginfo(current_time)
        self.af.write_logs(key,cont_list,stdout_list[0],step_list,return_dict,servername='vms',end=False)
        for server,stdout in zip(server_list,stdout_list):
            self.af.write_logs(key,cont_list,stdout,step_list,return_dict,servername=server)

    def get_streamid(self,ret):
        ret = json.loads(ret)
        streamid = ret['data'][0]['streamId']
        return streamid
    
    def content_format(self,content,streamid=None):
        for keyword,value in keyword_dict.items():
            if keyword in content:
                content = content.replace(keyword,value)
        if '${streamId}' in content:
            if not streamid:
                content = content.replace('${streamId}',streamId)
            else:
                content = content.replace('${streamId}',streamid)
        return content
    
    def run_case(self):
        cont_list = []
        step_list = []
        host_list = []
        streamid_list = []
        return_dict = {}
        case_dict = self.get_case_step()
        for key,value in case_dict.items():
            current_time = self.get_current_time()
            for step in value:
                num,st,act_type,host,port,content,params,expected,actual,desc = step
                host_list.append(host)
                if hasattr(self.mr, act_type.upper()):
                    params = self.content_format(params)
                    ret = getattr(self.mr,act_type.upper())(host,int(port),content,params)
                    return_dict[st] = ret
                    time.sleep(5)
                    try:
                        streamid = self.get_streamid(ret)
                        streamid_list.append(streamid)
                    except:
                        pass
                elif act_type.upper() == "RELATED":
                    try:
                        params = self.content_format(params,streamid_list[0])
                        content = self.content_format(content,streamid_list[0])
                        if content.startswith('/'):
                            #params = '{"streamId":"%s"}'%streamid_list[0]
                            ret = self.mr.GET(host, int(port), content, params)
                            return_dict[st] = ret
                            time.sleep(5)
                        elif content.startswith('STREAM:'):
                            val = self.get_redis_hash(host,redis_passwd,content,redis_port)
                            val = val if val else ['redis value is None!']
                            return_dict[st] = val 
                        streamid_list.pop(0)
                    except Exception as e:
                        print(act_type+':'+str(e))
                    
                elif act_type.upper() == "SHELL":
                    content = self.content_format(content)
                    self.ro.ssh_client(host,ssh_user,ssh_passwd,int(port))
                    if not content.endswith('&'):
                        stdout = self.ro.exec_command(content)
                        return_dict[st] = stdout
                    else:
                        stdout = self.ro.exec_command(content,nohup=True)
                        return_dict[st] = stdout
                    self.ro.ssh_close()
                elif act_type.upper() == "REDIS":
                    content = self.content_format(content)
                    val = self.get_redis_hash(host,redis_passwd,content,redis_port)
                    val = val if val else ['redis value is None!']
                    return_dict[st] = val
                elif act_type.upper() == "MYSQL":
                    content = self.content_format(content)
                    val = self.query_mysql_data(mysql_host,mysql_user,mysql_pwsswd,content)
                    return_dict[st] = val
                else:
                    print('not support keyword!')
                step_list.append(st)
                cont_list.append((act_type,content))           
            stdout_list = self.get_loginfo(current_time,host_list)
            try:
                server_list = ['VMS','CGS','MTS','MPS']
                self.af.write_logs(current_time[0],key,cont_list,stdout_list[0],step_list,return_dict,servername='VMS',end=False)
                for server,stdout in zip(server_list,stdout_list):
                    self.af.write_logs(current_time[0],key,cont_list,stdout,step_list,return_dict,servername=server)
                print(f"{key} write to logs successed!")
            except Exception as e:
                print(e)
                print(f"{key} write to logs failed!")
            finally:
                step_list = []
                cont_list = []
                return_dict = {}                
        
def run(casefile):
    rc = RunCase(casefile)
    rc.run_case()
    
if __name__ == "__main__":
    run('testcase.xlsx')
    #print(ssh_host)


