#coding:gbk
import numpy
import string
import datetime
import time

flag1 = 'start'
flag2 = 'finish'
timelength = 24
threadStartIndex = 29
DictName = {}
DictTime = {}
timeFormat = '%Y-%m-%d %H:%M:%S:%f'#时间格式
allSaveData = ''
DictTimeUse = {}
DictTimeSpace = {}
allTimeData = ''
allTimeList = []

def SaveInfo(line,flag):
    global allSaveData
    if(flag in line):
        #find thread id
        strFindThread = line[threadStartIndex:]
        threadEndIndex = strFindThread.find(']')
        resThreadID = strFindThread[0:threadEndIndex]
        
        startIndex = line.find(flag)
        interfaceStr = line[startIndex:]#get all interface name
        resStrTime = line[1:timelength]#get time
        allSaveData += resStrTime+'--'+resThreadID+'--' + interfaceStr
        
        ifArr = interfaceStr.split('|')#判断命令是否有效
        if(len(ifArr) < 3):
            return 0,'-1','-1','-1'
        lastIFName = ifArr[-2]#get last name
        resStrName = lastIFName.strip()#去除空格
        return 1,resStrTime,resStrName,resThreadID#多个返回参数
    return 0,'-1','-1','-1'

def GetTimeInterval(strtime1,strtime2):
    time1  = datetime.datetime.strptime(strtime1,timeFormat)
    time2  = datetime.datetime.strptime(strtime2,timeFormat)
    timeInterval = (time2-time1).total_seconds()
    return timeInterval

def GetInterfaceTime(threadid,finishtime):
    if threadid in DictName:
        startname = DictName.get(threadid)
        starttime = DictTime.get(startname)
        time1  = datetime.datetime.strptime(starttime,timeFormat)
        time2  = datetime.datetime.strptime(finishtime,timeFormat)
        timeInterval = (time2-time1).total_seconds()
        return timeInterval
    return 0

def DelLastItem(threadid):
    if threadid in DictName:
        tempname = DictName.get(threadid)
        del DictName[threadid]
        del DictTime[tempname]

def UpdateTimeUse(threadid,timeuse):
    global DictTimeUse,DictTimeSpace
    alltimeuse = 0
    if threadid in DictTimeUse:
        alltimeuse = DictTimeUse.get(threadid)
    DictTimeUse[threadid] = timeuse+alltimeuse

def UpdateTimeSpace(threadid,timespace):
    global DictTimeUse,DictTimeSpace
    alltimespace = 0
    if threadid in DictTimeSpace:
        alltimespace = DictTimeSpace.get(threadid)
    DictTimeSpace[threadid] = timespace+alltimespace

def CalculateAllTime(strtime,threadid,strname):
    global allTimeData,allTimeList
    if(len(allTimeList)>0):
        timeInterval = GetTimeInterval(allTimeList[-1],strtime)
        if(timeInterval>=0):
            allTimeList.append(strtime)
            allTimeData += strtime+'--'+threadid+'--'+strname+'\n'
    else:
        allTimeList.append(strtime)
        allTimeData += strtime+'--'+threadid+'--'+strname+'\n'

def LoadData(strfile):
    global allSaveData,DictTimeUse,DictTimeSpace
    lines=[]
    with open(strfile) as pFile:
        lines = pFile.readlines()
    for line in lines:
        res1,strTime,strName,threadID = SaveInfo(line,flag1)
        if(res1 == 1):
            CalculateAllTime(strTime,threadID,strName)
            timespace = GetInterfaceTime(threadID,strTime)
            UpdateTimeSpace(threadID,timespace)
            if(timespace > 0.1):
                print ('\ntimespace-->',threadID,'--',strName,'--',timespace,'\n')
            DelLastItem(threadID)
            DictName[threadID] = strName
            DictTime[strName] = strTime
            
        res2,strTime,strName,threadID = SaveInfo(line,flag2)
        if(res2 == 1):
            CalculateAllTime(strTime,threadID,strName)
            timeuse = GetInterfaceTime(threadID,strTime)
            UpdateTimeUse(threadID,timeuse)
            if(timeuse > 0.1):
                print (strName,'--',timeuse)
            allSaveData += strName + '--' + str(timeuse) + '\n'
            del DictName[threadID]
            del DictTime[strName]
            DictName[threadID] = strName
            DictTime[strName] = strTime
            
    
            
logpath = 'G:/iMAGESServer/branches/Version2/Bin/Win32/Server/MinGW/Debug/SpiderSightServer/Log/log.log'
LoadData(logpath)
now_time = datetime.datetime.now()
time_str = datetime.datetime.strftime(now_time,'%Y%m%d_%H_%M_%S')
outfilepath = time_str + '_logAnalysis.txt'
outfilepath = 'test.txt'
with open(outfilepath,'w') as saveFile:#写入数据到文件
    saveFile.write(allSaveData+'\n\n'+allTimeData)
print ('end')
print ('DictTimeUse:',DictTimeUse)
print ('DictTimeSpace:',DictTimeSpace)
print ('all time use:',GetTimeInterval(allTimeList[0],allTimeList[-1]))

pausett = input('pause')
