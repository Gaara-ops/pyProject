#coding:gbk
import numpy
import string
import datetime
import time
#i want to create a tag
flag1 = 'start'
flag2 = 'finish'
timelength = 24
threadlength = 30
StartDict = {}
FinishDict = {}

strTime1 = ''
strTime2 = ''
strName1 = ''
strName2 = ''
lastTime = ''
lastName = ''
timeFormat = '%Y-%m-%d %H:%M:%S:%f'#时间格式
allSaveData = ''
timeSpace = 0
timeUse = 0;
inVA = 0;
#其他判断
strTimeOther1 = ''
strTimeOther2 = ''
strCaSoring = "CalcificationScoreCalculation"
strStraighten = "GenerateStraightenVolume"
strAreaCurve = "ComputeAreaCurve"
def GetOtherFlagInfo(line):
    global allSaveData,strTimeOther1,strTimeOther2
    if(inVA == 0):
        return 0,'-1','-1'
    str1 = strCaSoring + " Begin"
    str2 = strCaSoring + " End"
    str3 = strStraighten + " Begin"
    str4 = strStraighten + " End"
    str5 = strAreaCurve + " Begin"
    str6 = strAreaCurve + " End"
    isstr = "";
    strtype = 1;
    if(str1 in line):
        isstr = str1
        strtype = 1
    elif(str2 in line):
        isstr = str2
        strtype = 2
    elif(str3 in line):
        isstr = str3
        strtype = 1
    elif(str4 in line):
        isstr = str4
        strtype = 2
    elif(str5 in line):
        isstr = str5
        strtype = 1
    elif(str6 in line):
        isstr = str6
        strtype = 2
    if(isstr == ""):
        return 0,'-1','-1'
    strTime = line[1:timelength]
    allSaveData += strTime + '--' + isstr+ '\n'
    if(strtype == 1):
        strTimeOther1 = strTime
    elif(strtype == 2):
        strTimeOther2 = strTime
        time1  = datetime.datetime.strptime(strTimeOther1,timeFormat)
        time2  = datetime.datetime.strptime(strTimeOther2,timeFormat)
        timeInterval = (time2-time1).total_seconds()
        print ('************',isstr,'--',timeInterval,'\n')
    

def SaveInfo(line,flag,strTime,strName):
    global allSaveData,StartDict,FinishDict#声明为全局变量
    if(flag in line):#判断字符串line是否包含字符串flag
        startIndex = line.find(flag)#查找flag在line中位置
        interfaceStr = line[startIndex:]#获取从某一位置到结束的字符串
        strTime = line[1:timelength]#获取从1到x处的字符串
        allSaveData += strTime + '--' + interfaceStr#字符串拼接
        ifArr = interfaceStr.split('|')#字符串分割
        if(len(ifArr) < 3):#判断数组的长度
            return 0,'-1','-1'
        lastIFName = ifArr[-2]#获取数组中倒数第二个元素
        strName = lastIFName.strip()#去除空格
        return 1,strTime,strName#多个返回参数
    return 0,'-2','-2'

def LoadData(strfile):
    global allSaveData,strName1,strName2,strTime1,strTime2
    global lastTime,lastName,timeSpace,timeUse
    global StartDict,FinishDict
    global inVA,strTimeOther1,strTimeOther2
    lines=[]
    with open(strfile) as pFile:#打开文件
        """
        读取所有文件,注意读取后文件指针偏移至最后
        allData = (pFile.read())
        """
        lines = pFile.readlines()#读取所有行
    #逐行读取文件
    for line in lines:
        res1,strTime,strName = SaveInfo(line,flag1,strTime1,strName1)
        if(res1 == 1):
            strTime1 = strTime
            strName1 = strName
        if(res1 == 1 and strName1 == "StartVesselAnalysis"):
            strTimeOther1 = ''
            strTimeOther2 = ''
            inVA = 1
        res2,strTime,strName = SaveInfo(line,flag2,strTime2,strName2)
        if(res2 == 1):
            strTime2 = strTime
            strName2 = strName
        if(res2 == 1 and strName2 == "StartVesselAnalysis"):
            strTimeOther1 = ''
            strTimeOther2 = ''
            inVA = 0
        
        GetOtherFlagInfo(line)
        
        if(strTime1!='' and lastTime!='' and res1):
            time1  = datetime.datetime.strptime(lastTime,timeFormat)
            time2  = datetime.datetime.strptime(strTime1,timeFormat)
            timeInterval = (time2-time1).total_seconds()
            timeSpace += timeInterval
            if timeInterval>0.1:
                print ('\n',lastName,'->',strName1,'--',timeInterval,'\n')
        if((strName1 == strName2) and strName1!=''):
            #字符串转datetime
            time1  = datetime.datetime.strptime(strTime1,timeFormat)
            time2  = datetime.datetime.strptime(strTime2,timeFormat)
            #datetime时间间隔计算
            timeInterval = (time2-time1).total_seconds()
            timeUse += timeInterval
            if timeInterval>0.1:
                print (strName1,'--',timeInterval)
            allSaveData += strName1 + '--' + str(timeInterval) + '\n'
            lastTime = strTime2
            lastName = strName2
            strName1 = strName2 = ''
            
logpath = 'G:/iMAGESServer/branches/Version2/Bin/Win32/Server/MinGW/Debug/SpiderSightServer/Log/log.log'
LoadData(logpath)
now_time = datetime.datetime.now()
time_str = datetime.datetime.strftime(now_time,'%Y%m%d_%H_%M_%S')
outfilepath = time_str + '_logAnalysis.txt'
outfilepath = 'test.txt'
with open(outfilepath,'w') as saveFile:#写入数据到文件
    saveFile.write(allSaveData)
print ('end')
print ('allTime:',timeUse+timeSpace)
print ('timeUse:',timeUse)
print ('timeSpace:',timeSpace)
pausett = input('pause')
