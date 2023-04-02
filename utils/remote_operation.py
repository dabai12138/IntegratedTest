# -*- coding: utf-8 -*-

import paramiko
import pexpect
import datetime
import os,sys
import time


class RemoteOperation(object):
    def __init__(self):
        pass
    
    def ssh_client(self,host,user,passwd,port=22):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=host,
                         port=port,
                         username=user,
                         password=passwd,
                         timeout=300,
                         allow_agent=False,
                         look_for_keys=False)
        except Exception:
            print("connect error!")
    
    def _sftp(self):
        try:
            self.t = paramiko.Transport((self.host,self.port))
            self.t.connect(username=self.user,password=self.passwd)
            self.sftp = paramiko.SFTPClient.from_transport(self.t)
        except Exception:
            print("connect error!")
        
    
    def upload(self,local_path,remote_path):
        self._sftp()
        files = os.listdir(local_path)
        for i in files:
            self.sftp.put(os.path.join(local_path,i),os.path.join(remote_path,i))
        return
        
    def download(self,local_path,remote_path):
        self._sftp()
        files = self.sftp.listdir(remote_path)
        for i in files:
            self.sftp.get(os.path.join(remote_path,i),os.path.join(local_path,i))

    def exec_command(self,command,nohup=False):
        if not nohup:
            stdin,stdout,stderr = self.ssh.exec_command(command,get_pty=True)  
            #print(stdout.readlines())
            return stdout.readlines()
        else: 
            try:
                # transport = self.ssh.get_transport()
                # channel = transport.open_session()
                # ret = channel.exec_command(command)
                invoke = self.ssh.invoke_shell()
                ret = invoke.send(command+'\n')
                time.sleep(2)
            except Exception as e:
                ret = e
            return str(ret)

    def ssh_close(self):
        try:
            self.ssh.close()
            print("ssh close successed")
        except Exception:
            print("ssh close failed")
        
    def sftp_close(self):
        try:
            self.t.close()
            print("sftp closed successed")
        except Exception:
            print("sftp close failed")

if __name__ == "__main__":
    ro = RemoteOperation()
    ro.ssh_client("192.168.6.18","root","bwin3456")
    #cmd = 'nohup /root/wj/CGS/CGS &>/dev/null &'
    #cmd = 'cd wj/CGS;source ~/.bashrc;nohup ./CGS &>/dev/null \n'
    #cmd = 'cd wj/st-load/objs;nohup ./st_rtmp_load -c 1 -r rtmp://192.168.2.184:1035/live/34020000001320000033_MAIN >/dev/null 2>&1 &'
    cmd = "cd /home/v3.0/CGS/CGS_log;cat cgs_INFO_20201203-164648.27007.log|grep -i channelid"
    cmd2 = "cd /home/v3.0/CGS/CGS_log;cat cgs_INFO_20201203-170328.27007.log|grep -i channelid"
    ret = ro.exec_command(cmd)
    ret2 = ro.exec_command(cmd2)
    ll = []
    for i in ret:
        a = i.split(":")[1].strip(',\r\n')
        ll.append(eval(a)) 
    for i in ret2:
        a = i.split(":")[1].strip(',\r\n')
        ll.append(eval(a))
    ro.ssh_close()
    ll=list(set(ll))
    for i,v in enumerate(ll):
        v.strip('3402000000131000')
    
