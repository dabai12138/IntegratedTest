# !/usr/bin/python 
# -*- coding: utf-8 -*-

import os
import re
from configparser import ConfigParser
basepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


from utils.act_conf import ReadConf




rc = ReadConf()
ssh_host = rc.get_value('HOST', 'ssh_host')
ssh2_host = rc.get_value('HOST', 'ssh2_host')
ssh_user = rc.get_value('USER', 'ssh_user')
ssh_passwd = rc.get_value('PASSWD', 'ssh_passwd')      
mysql_host = rc.get_value('HOST', 'mysql_host')
mysql_user = rc.get_value('USER', 'mysql_user')
mysql_pwsswd = rc.get_value('PASSWD','mysql_pwsswd')
mysql_port = rc.get_value('PORT', 'mysql_port')
redis_host = rc.get_value('HOST', 'redis_host')
redis_passwd = rc.get_value('PASSWD','redis_passwd')
redis_port = rc.get_value('PORT', 'redis_port')     
vms_host = rc.get_value('HOST', 'vms_host')
cgs_host = rc.get_value('HOST', 'cgs_host')
mps_host = rc.get_value('HOST', 'mps_host')
mts_host = rc.get_value('HOST', 'mts_host')
vms_port = rc.get_value('PORT', 'vms_port')
cgs_port = rc.get_value('PORT', 'cgs_port')
mps_port = rc.get_value('PORT', 'mps_port')
mts_port = rc.get_value('PORT', 'mts_port')
vms_logpath = rc.get_value('LOGPATH', 'vms_logpath')
vms2_logpath = rc.get_value('LOGPATH', 'vms2_logpath')
vms3_logpath = rc.get_value('LOGPATH', 'vms3_logpath')
cgs_logpath = rc.get_value('LOGPATH', 'cgs_logpath')
mts_logpath = rc.get_value('LOGPATH', 'mts_logpath')
mps_logpath = rc.get_value('LOGPATH', 'mps_logpath') 

jar_package = rc.get_value('KEYWORD', 'jar_package')
serial = rc.get_value('KEYWORD', 'serial')
deviceId = rc.get_value('KEYWORD', 'deviceId')
channelId = rc.get_value('KEYWORD', 'channelId')
streamId = rc.get_value('KEYWORD', 'streamId')

cgs_cmd = "netstat -anp|grep -i :%s|grep -v java|head -n 1|awk '{print $7}'|cut -d / -f 1"%str(cgs_port)
mts_cmd = "netstat -anp|grep -i :%s|grep -v java|head -n 1|awk '{print $7}'|cut -d / -f 1"%str(mts_port)
mps_cmd = "netstat -anp|grep -i :%s|grep -v java|head -n 1|awk '{print $7}'|cut -d / -f 1"%str(mps_port)

format_time = [
            "%Y-%m-%d %H:%M:%S",
            "%Y%m%d %H:%M:%S",
            "%Y%m%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S"
            ]

server_list = ['vms','cgs','Mts','mps']

logpath_list = [
            vms_logpath,
            cgs_logpath,
            mts_logpath,
            mps_logpath
            ]

keyword_dict = {
            '${jar_package}':jar_package,
            '${serial}':serial,
            '${deviceId}':deviceId,
            '${channelId}':channelId,
            '${vms_logpath}':vms_logpath,
            '${vms2_logpath}':vms2_logpath,
            '${vms3_logpath}':vms3_logpath
            }