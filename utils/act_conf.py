# -*- coding: utf-8 -*-

from configparser import ConfigParser
from utils import *
import os,sys


conf_path = os.path.join(basepath,'conf','base_conf.conf') 

    
class ReadConf(object):
    def __init__(self,confpath=conf_path):
        self.conf = ConfigParser()
        self.conf.read(confpath)
        
    def get_sections(self):
        return self.conf.sections()
    
    def get_options(self,section):
        return self.conf.options(section)
    
    def get_value(self,section,option):
        return self.conf.get(section,option)

if __name__ == "__main__":
    rc = ReadConf()
    ret = rc.get_value('HOST','host')
    print(ret)