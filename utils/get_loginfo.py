# -*- coding: utf-8 -*-

import os,sys
import datetime,time
from utils.remote_operation import RemoteOperation
from utils import *


#2020-10-22 10:11:00



class GetLogs(object):
    
    def __init__(self,RO):
        self.RO = RO
    
    def _get_log(self,logdir,keyword):
        if keyword == 'cgs':
            cgs_pid = self._exec_shell(cgs_cmd)
            cgs_command = "ls -lt %s|grep -i cgs_INFO|grep %s.log|head -n 1|awk '{print $9}'"%(logdir,cgs_pid[0])
            logname = self._exec_shell(cgs_command)
        elif keyword == 'Mts':
            mts_pid = self._exec_shell(mts_cmd)
            mts_command = "ls -lt %s|grep -i %s.log|head -n 1|awk '{print $9}'"%(logdir,mts_pid[0])
            logname = self._exec_shell(mts_command)
        elif keyword == 'mps':
            mps_command = "ls -lt %s |grep -i mps|head -n 2|awk '{print $9}'"%logdir
            logname = self._exec_shell(mps_command)
        else:
            logname = [keyword+'.log']
        return logname
    
    def _exec_shell(self,command):
        res = self.RO.exec_command(command)
        for index,r in enumerate(res):
            res[index] = r.strip('\r\n')
        return res
        
    def ssh_open(self,host, user, passwd, port=22):
        self.RO.ssh_client(host, user, passwd, port)
    
    def ssh_close(self):
        self.RO.ssh_close()
        
    def get_loginfo(self,curr_time,logdir,time_format,keyword):
        try:
            logsname = self._get_log(logdir, keyword)
            sum_std = []
            for logname in logsname:
                print(curr_time)
                current_time = curr_time
                logfile = logdir+"/"+logname
                n = 0
                while True:
                    command = f"sed -n '/{current_time}/,$p' {logfile}"
                    stdout = self.RO.exec_command(command)
                    if stdout:
                        break
                    else:
                        if keyword == 'vms' or keyword == 'mps':
                            t = datetime.datetime.strptime(str(current_time),time_format)
                            current_time = t+datetime.timedelta(seconds=1)
                        else:
                            if n == 0:
                                t = datetime.datetime.strptime(str(current_time),time_format)
                            else:
                                year = datetime.datetime.now().year
                                t = datetime.datetime.strptime(str(year)+str(current_time),time_format)
                            current_time = t+datetime.timedelta(seconds=1)
                            current_time = str(current_time).replace('-','')[4:]
                        n+=1
                        if n>30:
                            #stdout = [f'{keyword} loginfo is Null']
                            break
                sum_std+=stdout
            return sum_std
        except Exception as e:
            print(keyword+str(e))
   
if __name__ == "__main__":
    RO = RemoteOperation()
    RO.ssh_client('192.168.2.184', 'root', 'bwin3456')
    gl = GetLogs(RO)
    command = "ls -lt /root/wj/MPS/MPS |grep -i java"
    pid = gl._exec_shell(command)
    print(pid)
    RO.ssh_close()
