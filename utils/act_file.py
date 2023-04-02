# -*- coding: utf-8 -*-
#!/usr/bin/python


import os,sys
import time
import re
import xlrd
import pandas as pd
from xlutils.copy import copy
from utils import *


log_path = os.path.join(basepath,'logs')
case_path = os.path.join(basepath,'testcase')
now_time = time.strftime("%Y%m%d-%H",time.localtime(time.time()))


class ActFile(object):

    def __init__(self):
        pass

    def path_format(self,name="V3.0"):
        file_name = name+'-'+now_time+'.log'
        file_path = os.path.join(log_path,file_name)
        return file_path

    def write_logs(self,current_time,casename,cont_list,context,step_list,return_dict,servername='VMS',end=True):
        file_path = self.path_format()
        filter_list = []
        filter_key_list = ['v1/mts_load','v1/mps_load','mem_kbyte','v1/stream_data','{"streamId":[]}','get MtsLoad successful','get StreamList successful','get MtsLoad','deviceSubscribe','Content is empty']
        with open(file_path,'a+',encoding='utf-8',newline='') as fp:
            if end:    
                fp.write('\n'+'*'*50+str(servername)+'*'*50+'\n')
                for cont in context:
                    for f in filter_key_list:
                        if f in cont:
                            filter_list.append(cont)
                context = [cont for cont in context if cont not in filter_list]
                if context:                
                    for cont in context:
                        fp.write(cont)
                        fp.flush()
                else:
                    fp.write(servername+'Content is filtered out')
                    fp.flush()
                fp.write('\n'+'*'*100+'\n')
                fp.flush()
            else:
                fp.write("\n"+"="*100+'\n')
                fp.write("="*50+casename+"="*50+'\n')
                fp.write("="*50+current_time[5:]+"="*50+'\n')
                for step,cl in zip(step_list,cont_list):
                    content = return_dict[step]
                    fp.write(str(step)+':'+str(cl[0])+' '+str(cl[1])+'\n')
                    if type(content) == dict:
                        for k,v in content.items():
                            if type(k) == bytes:
                                fp.write(k.decode()+':'+v.decode()+'\n')
                            else:
                                fp.write(str(k)+':'+str(v)+'\n')
                    else:
                        fp.write('result:')
                        for cont in content:
                            if type(cont) == bytes:
                                fp.write(cont.decode())
                            else:
                                fp.write(str(cont))
                    fp.write('\n')
                fp.flush()

class ReadExcel(object):
    def __init__(self, filename):
        self.file = os.path.join(case_path, filename)
        self.rb = xlrd.open_workbook(self.file)

    # get all row data
    def get_rows(self, name='Sheet1'):
        table = self.rb.sheet_by_name(name)
        nrows = table.nrows
        rows = []
        for row in range(nrows):
            data = table.row_values(row)
            rows.append(data)
        return rows[1:]

    # get one row data
    def get_row(self, row, name='Sheet1'):
        table = self.rb.sheet_by_name(name)
        data = table.row_values(row)
        return data

    # get all col data
    def get_cols(self, name='Sheet1'):
        table = self.rb.sheet_by_name(name)
        ncols = table.ncols
        cols = []
        for col in range(ncols):
            data = table.col_values(col)
            cols.append(data)
        return cols

    
class UpdateExcel(ReadExcel):
    def __init__(self,filename):
        super(UpdateExcel,self).__init__(filename)
        self.file = os.path.join(case_path, filename)
    
    #UNDO
    def update(self,row,col,content,name='Sheet1'):
        try:
            wb = copy(self.rb)
            ws = wb.get_sheet(name)
            ws.write(row,col,content)
            wb.save(self.file)
            print("update data successed!")
        except Exception as e:
            print(e)
            print("update data failed!")
    

if __name__ == "__main__":
    # me = ReadExcel("testcase.xlsx")
    # nrows = me.get_rows()
    # case_list = []
    # case_dict = {}
    # space_num = nrows.count(['', '', '', '', '', '', '', '', ''])
    # if space_num:
    #     for index,row in enumerate(nrows):     
    #         if row[0]:
    #             case_list.append(row)
    #             if len(case_dict) == space_num:
    #                 case_dict[case_list[0][0]] = nrows[index:]              
    #         else:
    #             case_dict[case_list[0][0]] = case_list
    #             case_list = []
    # else:
    #     case_dict[nrows[0][0]] = nrows
    # print(case_dict)
    # ue = UpdateExcel("testcase.xls")
    # ue.update()
    pass
    
        
            
