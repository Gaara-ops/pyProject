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
DictDataByThreadID = {}#the data of all thread
DictTimeUse = {}#interface time use
DictTimeSpace = {}#space time Use
allTimeData = ''
allTimeList = []#all time data

#other flag to find------------------------------------
OtherFlagList = ['CalcificationScoreCalculation','GenerateStraightenVolume','ComputeAreaCurve']
OtherFlagData = {}
def SaveOtherDataByThread(threadid,data):
    global OtherFlagData
    nowData = ''
    if threadid in OtherFlagData:
        nowData = OtherFlagData.get(threadid)
    OtherFlagData[threadid] = nowData+data


def GetOtherFlagInfo(line,flag):
    if flag in line:
        strFindThread = line[threadStartIndex:]
        threadEndIndex = strFindThread.find(']')
        resThreadID = strFindThread[0:threadEndIndex]
        resStrTime = line[1:timelength]#get time
        onelinedata = resStrTime+'--'+resThreadID+'--' + flag+'\n'
        SaveOtherDataByThread(resThreadID,onelinedata)

def FindOtherFlag(line):
    for tempfg in OtherFlagList:
        tempfg1 = tempfg + ' Begin'
        tempfg2 = tempfg + ' End'
        GetOtherFlagInfo(line,tempfg1)
        GetOtherFlagInfo(line,tempfg2)
        
#---------------------------------
def SaveDataByThread(threadid,data):
    global DictDataByThreadID
    nowData = ''
    if threadid in DictDataByThreadID:
        nowData = DictDataByThreadID.get(threadid)
    DictDataByThreadID[threadid] = nowData+data
        
#analysis one line info and save time and interface name
def SaveInfo(line,flag):
    if(flag in line):
        #find thread id
        strFindThread = line[threadStartIndex:]
        threadEndIndex = strFindThread.find(']')
        resThreadID = strFindThread[0:threadEndIndex]
        
        startIndex = line.find(flag)
        interfaceStr = line[startIndex:]#get all interface name
        resStrTime = line[1:timelength]#get time
        onelinedata = resStrTime+'--'+resThreadID+'--' + interfaceStr
        ifArr = interfaceStr.split('|')#判断命令是否有效
        if(len(ifArr) < 3):
            return 0,'-1','-1','-1'
        lastIFName = ifArr[-2]#get last name
        resStrName = lastIFName.strip()#remove the blank space
        SaveDataByThread(resThreadID,onelinedata)
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
    global DictTimeUse,DictTimeSpace
    lines=[]
    with open(strfile) as pFile:
        lines = pFile.readlines()
    for line in lines:
        FindOtherFlag(line)
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
                print (threadID,'--',strName,'--',timeuse)
            strTimeUse = strName + '--' + str(timeuse) + '\n'
            SaveDataByThread(threadID,strTimeUse)
            del DictName[threadID]
            del DictTime[strName]
            DictName[threadID] = strName
            DictTime[strName] = strTime

logpath = 'G:/iMAGESServer/branches/Version2/Bin/Win32/Server/MinGW/Debug/SpiderSightServer/Log/log.log'
#logpath = 'Unknow.log'
LoadData(logpath)
now_time = datetime.datetime.now()
time_str = datetime.datetime.strftime(now_time,'%Y%m%d_%H_%M_%S')
outfilepath = time_str + '_logAnalysis.txt'
outfilepath = 'test.txt'

def CalculateOtherFlagTime():
    for key,value in OtherFlagData.items():
        time1 = ''
        time2 = ''
        namearr = value.split('\n')
        for line in namearr:
            if 'Begin' in line:
                time1 = line[:timelength-1]
            if 'End' in line:
                time2 = line[:timelength-1]
            if time1 != '' and time2 != '':
                tempuse = GetTimeInterval(time1,time2)
                print (line[timelength:],'---',tempuse)
                time1=''
                time2=''

with open(outfilepath,'w') as saveFile:#write data to file
    for key,value in DictDataByThreadID.items():
        saveFile.write(key+'--\n'+value+'\n\n')
    for key,value in OtherFlagData.items():
        saveFile.write(key+'--\n'+value+'\n\n')

        
print ('end')
print ('DictTimeUse:',DictTimeUse)
print ('DictTimeSpace:',DictTimeSpace)
print ('all time use:',GetTimeInterval(allTimeList[0],allTimeList[-1]))
print ('\nOther interface use time:')
CalculateOtherFlagTime()
pausett = input('pause')

