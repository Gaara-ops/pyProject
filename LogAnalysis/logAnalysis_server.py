#coding:gbk
import numpy
import string
import datetime
import time

threadID = '140016022997056'
allSaveData = ''

def LoadData(strfile):
    global threadID,allSaveData
    with open(strfile) as pFile:
        for line in pFile:
            if(threadID in line):
                allSaveData += line
                
logpath = 'E:/pywork/LogAnalysis/Unknow.log'
LoadData(logpath)
now_time = datetime.datetime.now()
time_str = datetime.datetime.strftime(now_time,'%Y%m%d_%H_%M_%S')
outfilepath = time_str + '_logAnalysis_170.txt'
outfilepath = 'test.txt'
with open(outfilepath,'w') as saveFile:#写入数据到文件
    saveFile.write(allSaveData)
print ('end')
