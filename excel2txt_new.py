# -*- coding: utf-8 -*-
import json
import os
import re
import nltk
import xlwt
from xlwt import *

import xlrd
from datetime import date,datetime

def read_excel():
    #文件位置
    ExcelFile=xlrd.open_workbook(r'excel2txt.xls')  ##输入：标注后的业务数据 文件名
    #获取目标EXCEL文件sheet名
    print (ExcelFile.sheet_names())
    #------------------------------------
    #若有多个sheet，则需要指定读取目标sheet例如读取sheet2
    #sheet2_name=ExcelFile.sheet_names()[1]
    #------------------------------------
    #获取sheet内容【1.根据sheet索引2.根据sheet名称】
    #sheet=ExcelFile.sheet_by_index(1)
    sheet=ExcelFile.sheet_by_name('My Worksheet')
    #打印sheet的名称，行数，列数
    print (sheet.name,sheet.nrows,sheet.ncols)
    #获取整行或者整列的值
    #rows=sheet.row_values(2)#第三行内容
    #cols=sheet.col_values(1)#第二列内容
    #print (cols)
    #print (rows)
    #获取单元格内容
    #print (sheet.cell(1,1).value.encode('utf-8'))
    file = r'machine_learn_data.txt'  ##输出： 文件名
    with open(file, 'a+') as f:
        for r_id in range(sheet.nrows):  #sheet.nrows
            print(r_id)
            for l_id in range(3, 7):   #公司名， 地址， 电话， 传真
                #print(sheet.cell_value(r_id,l_id))
                if (sheet.cell_value(r_id,l_id).strip()!=""):
                    c = nltk.word_tokenize(sheet.cell_value(r_id,l_id))
                    for i in range(len(c)):
                        if(c[i] != '.' and c[i] != ',' and c[i] != ':'and c[i] != '/' and c[i] != '('and c[i] != ')'):
                            if (l_id == 3):
                                if i == 0:
                                    print(str(r_id), c[i], 'ORGB')
                                    f.write(str(r_id) + c[i] + ' ORGB' + '\n')  # 加\n换行显示
                                else:
                                    print(str(r_id), c[i], 'ORGI')
                                    f.write(str(r_id) + c[i] + ' ORGI' + '\n')  # 加\n换行显示
                            elif (l_id == 4):
                                if i == 0:
                                    print(str(r_id), c[i], 'ADRB')
                                    f.write(str(r_id) + c[i] + ' ADRB' + '\n')  # 加\n换行显示
                                else:
                                    print(str(r_id), c[i], 'ADRI')
                                    f.write(str(r_id) + c[i] + ' ADRI' + '\n')  # 加\n换行显示
                            elif (l_id == 5):
                                if i == 0:
                                    print(str(r_id), c[i], 'TELB')
                                    f.write(str(r_id) + c[i] + ' TELB' + '\n')  # 加\n换行显示
                                else:
                                    print(str(r_id), c[i], 'TELI')
                                    f.write(str(r_id) + c[i] + ' TELI' + '\n')  # 加\n换行显示
                            elif (l_id == 6):
                                if i == 0:
                                    print(str(r_id), c[i], 'FAXB')
                                    f.write(str(r_id) + c[i] + ' FAXB' + '\n')  # 加\n换行显示
                                else:
                                    print(str(r_id), c[i], 'FAXI')
                                    f.write(str(r_id) + c[i] + ' FAXI' + '\n')  # 加\n换行显示
            print('\n')
            f.write('\n')
        #print (sheet.row(1)[0].value.encode('utf-8'))

    #打印单元格内容格式
    #print (sheet.cell(1,0).ctype)

if __name__ == '__main__':
    read_excel()