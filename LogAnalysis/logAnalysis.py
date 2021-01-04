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
timeFormat = '%Y-%m-%d %H:%M:%S:%f'#time format
allSaveData = ''
DictTimeUse = {}
DictTimeSpace = {}
allTimeData = ''
allTimeList = []

#analysis one line info and save time and interface name
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
        resStrName = lastIFName.strip()#remove the blank space
        return 1,resStrTime,resStrName,resThreadID#return mul parameters
    return 0,'-1','-1','-1'

#get two time interval
def GetTimeInterval(strtime1,strtime2):
    time1  = datetime.datetime.strptime(strtime1,timeFormat)
    time2  = datetime.datetime.strptime(strtime2,timeFormat)
    timeInterval = (time2-time1).total_seconds()
    return timeInterval

#get one interface used time
def GetInterfaceTime(threadid,finishtime):
    if threadid in DictName:
        startname = DictName.get(threadid)
        starttime = DictTime.get(startname)
        time1  = datetime.datetime.strptime(starttime,timeFormat)
        time2  = datetime.datetime.strptime(finishtime,timeFormat)
        timeInterval = (time2-time1).total_seconds()
        return timeInterval
    return 0

#delete the last item in DictName and DictTime
def DelLastItem(threadid):
    if threadid in DictName:
        tempname = DictName.get(threadid)
        del DictName[threadid]
        del DictTime[tempname]

#update the time of interface had used
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
    with open(strfile,encoding='utf-8') as pFile:
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
            
    

#G:\iMAGESServer\branches\Version1\Bin\Win32\Server\MinGW\Debug\SpiderSightServer\Log
logpath = 'G:/iMAGESServer/branches/Version5/Bin/Win32/Server/MinGW/Debug/SpiderSightServer/Log/log.log'
LoadData(logpath)
now_time = datetime.datetime.now()
time_str = datetime.datetime.strftime(now_time,'%Y%m%d_%H_%M_%S')
outfilepath = time_str + '_logAnalysis.txt'
outfilepath = 'test.txt'
with open(outfilepath,'w') as saveFile:#write data to file
    saveFile.write(allSaveData+'\n\n'+allTimeData)
print ('end')
print ('DictTimeUse:',DictTimeUse)
print ('DictTimeSpace:',DictTimeSpace)
print ('all time use:',GetTimeInterval(allTimeList[0],allTimeList[-1]))

pausett = input('pause')
