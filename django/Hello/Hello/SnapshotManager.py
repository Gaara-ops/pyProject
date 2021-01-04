#coding: UTF-8
from django.conf.urls import url
#from django.contrib import admin
from django.http import HttpResponse
from django.http import JsonResponse
import json
import os
import struct
import sys
import datetime

def GetSnapshotResult(request):
    #print("request.body={}".format(request.body))
    print("GetSnapshotResult")
    if request.method == "POST":
        JsonBuffer = json.loads(request.body.decode('utf-8'))
        institutionID = JsonBuffer["institutionID"]
        studyInstanceUID = JsonBuffer["studyInstanceUID"]
        modeName = JsonBuffer["modeName"]
        instanceName = JsonBuffer["instanceName"]
        sourceName = JsonBuffer["sourceName"]
        if institutionID == '':
            institutionID = '100000'
        print("institutionID:" + institutionID)
        print("studyInstanceUID:" + studyInstanceUID)
        print("modeName:" + modeName)
        print("instanceName:" + instanceName)
        print("sourceName:" + sourceName)

        userID = JsonBuffer["userID"]
        typeID = JsonBuffer["typeID"]
        functionName = JsonBuffer["functionName"]
        snapshotID = JsonBuffer["snapshotID"]
        if userID == '':
            userID = '88'
        print("userID:" + userID)
        print("typeID:" + typeID)
        print("functionName:" + functionName)
        print("snapshotID:" + snapshotID)
        #dirPath = os.path.abspath(os.path.dirname(os.getcwd())) + "/Snapshot"
        dirPath = 'G:'
        filePath = dirPath + "/" + institutionID + "/" + studyInstanceUID + "/" + modeName + "/" + instanceName + "/" + sourceName + "/" + userID + "/"
        if(not os.path.exists(filePath)):
            os.makedirs(filePath)
        filePath = filePath + functionName
        print("FilePath:" + filePath)
        if typeID == "1":
            if os.path.exists(filePath):
                f = open(filePath, 'r', encoding='UTF-8')
                snapshotResult = f.read()
                #DataJson = json.dumps(snapshotResult, ensure_ascii=False)
                jsonData = []
                dataBuffer = {"dataBuffer": snapshotResult}
                jsonData.append(dataBuffer)
                rtnJson = {"resultCode": "0", "isSuccess": True, "resultMsg": "0", "jsonData": jsonData}
                t = json.dumps(rtnJson, ensure_ascii=False)
                f.close()
                return HttpResponse(t)
            else:
                rtnJson = {"resultCode": "-1", "isSuccess": False, "resultMsg": "获取失败", "jsonData": ""}
                return JsonResponse(rtnJson)
        else:
            print("POST RAW")
            if os.path.exists(filePath):
                f = open(filePath, 'rb')
                t = f.read()
                f.close()
                return HttpResponse(t)
            else:
                rtnJson = {"resultCode": "-1", "isSuccess": False, "resultMsg": "获取失败", "jsonData": ""}
                return JsonResponse(rtnJson)
    else:
        rtnJson = {"resultCode": "-1", "isSuccess": False, "resultMsg": "获取失败", "jsonData": ""}
        return JsonResponse(rtnJson)

def SubmitSnapshotResult(request):
    #print("request.body={}".format(request.body))
    print("SubmitSnapshotResult")
    if request.method == "POST":
        stream = format(request.body)
        contentLength = sys.getsizeof(request.body) - 16 #len.
        contentLengthttt = len(request.body) - 16  # len
        print("contentLength:" + str(contentLength) + "  --  contentLengthttt:"+ str(contentLengthttt))
        strUnpack = "<qq{}s".format(str(contentLengthttt))
        print("strUnpack:" + strUnpack)
        dataLength, headerLength, content = struct.unpack(strUnpack, request.body)
        print("dataLength:" + str(dataLength))
        print("headerLength:" + str(headerLength))
        #print("content:" + str(content))

        #解析头和数据
        bodyLength = contentLengthttt - headerLength
        contentHeader,contentBody = struct.unpack("<{}s{}s".format(str(headerLength), str(bodyLength)), content)

        #print("contentHeader:" + str(contentHeader))
        #print("contentBody:" + str(contentBody))

        JsonBuffer = json.loads(contentHeader.decode('utf-8'))
        Meta = JsonBuffer["Meta"]
        #dirPath = os.path.abspath(os.path.dirname(os.getcwd())) + "/Snapshot"
        dirPath = 'G:'
        #这里先解析一个的
        unpackParam = ""
        countData = 0
        for info in Meta:
            DataSize = info["DataSize"]
            TextSize = info["TextSize"]
            print("DataSize:" + str(DataSize) + "  " + str(TextSize))
            countData = countData + 1
            unpackParam = unpackParam + "{}s{}s".format(str(TextSize), str(DataSize))

        unpackParam = "<" + unpackParam
        print("unpackParam:" + str(unpackParam))
        streamData = []
        streamData = struct.unpack(unpackParam, contentBody)

        count = 0
        time1_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for info in Meta:
            #print("info:" + str(info))
            DataSize = info["DataSize"]
            TextSize = info["TextSize"]
            Type = info["Type"]
            print("DataSize:" + str(DataSize) + "  " +str(TextSize))
            if int(TextSize) > 0:
                TextContent = streamData[2 * count]
                BodyContent = streamData[2 * count + 1]
                #print("TextContent: ",TextContent)
                #TextContent, BodyContent = struct.unpack("<{}s{}s".format(str(TextSize),str(DataSize)), contentBody)
                mataInfo = json.loads(TextContent.decode('gbk').replace("\n",""))
                #print("mataInfo:" + str(mataInfo))
                institutionID = mataInfo["institutionID"]
                studyInstanceUID = mataInfo["studyInstanceUID"]
                modeName = mataInfo["modeName"]
                instanceName = mataInfo["instanceName"]
                sourceName = mataInfo["sourceName"]
                userID = mataInfo["userID"]
                userName = mataInfo["userName"]
                typeID = mataInfo["typeID"]
                functionName = mataInfo["functionName"]
                if institutionID == '':
                    institutionID = '100000'
                if userID == '':
                    userID = '88'
                if userName == '':
                    userName = 'wg0'
                #test save snaplist
                SetSnapList(institutionID, studyInstanceUID, modeName, instanceName, sourceName, userID, userName, functionName, time1_str)

                filePath = dirPath + "/" + institutionID + "/" + studyInstanceUID + "/" + modeName + "/" + instanceName + "/" + sourceName + "/" + userID + "/"
                if (not os.path.exists(filePath)):
                    os.makedirs(filePath)
                filePath = filePath + functionName
                print("filePath:" + filePath)
                if typeID == "1":
                    snapshotResult = mataInfo["snapshotResult"]
                    f = open(filePath, 'w+', encoding='UTF-8')
                    DataDest = json.dumps(snapshotResult, ensure_ascii=False)
                    t = f.write(str(DataDest))
                    f.close()
                else:
                    f = open(filePath, 'wb')
                    t = f.write(BodyContent)
                    f.close()

                    #return  HttpResponse("2 SnapshotSubmit!")
            count = count + 1

        rtnJson = {"resultCode": "0", "isSuccess": True, "resultMsg": "0"}
        return JsonResponse(rtnJson)
    else:
        rtnJson = {"resultCode": "-1", "isSuccess": False, "resultMsg": "获取失败", "jsonData": ""}
        return JsonResponse(rtnJson)

def GetSnapshotList(request):
    #print("request.body={}".format(request.body))
    print("GetSnapshotList")
    if request.method == "POST":
        JsonBuffer = json.loads(request.body.decode('utf-8'))
        institutionID = JsonBuffer["institutionID"]
        studyInstanceUID = JsonBuffer["studyInstanceUID"]
        modeName = JsonBuffer["modeName"]
        instanceName = JsonBuffer["instanceName"]
        sourceName = JsonBuffer["sourceName"]
        userID = JsonBuffer["userID"]
        userName = JsonBuffer["userName"]
        if institutionID == '':
            institutionID = '100000'
        if userID == '':
            userID = '88'
        if userName == '':
            userName = 'wg0'

        #dirPath = os.path.abspath(os.path.dirname(os.getcwd())) + "/Snapshot"
        dirPath = 'G:'
        #filePath = dirPath + "/" + institutionID + "/" + studyInstanceUID + "/" + modeName + "/" + instanceName + "/" + sourceName + "/" + userID + "/" + "SnapShotList.json"
        filePath = dirPath + "/" + institutionID + "/" + studyInstanceUID + "/" + modeName + "/" + instanceName + "/" + sourceName + "/"

        isDir = os.path.isdir(filePath)  # 判断是否是文件夹
        if not isDir:  # 不是文件夹直接返回
            print("not a dir")
            return HttpResponse("not a dir")
        filelist = os.listdir(filePath)  # 获取目录名列表
        jsonData = []
        for i in filelist:  # 遍历根目录
            filetmp = os.path.join(filePath, i)  # 连接目录与文件名
            filetmp = filetmp + "/" + "SnapShotList.json"
            if (os.path.exists(filetmp)):
                f = open(filetmp, 'r', encoding='UTF-8')
                FileData = f.read()
                FileJsonData = json.loads(FileData)
                jsonData.append(FileJsonData)
        rtnJson = {"resultCode": "0", "isSuccess": True, "resultMsg": "0", "jsonData": jsonData}
        t = json.dumps(rtnJson, ensure_ascii=False)
        f.close()
        return HttpResponse(t)

def SetSnapList(institutionID, studyInstanceUID, modeName, instanceName, sourceName, userID, userName, functionName, time1_str):
    print("SetSnapList:")
    
    #dirPath = os.path.abspath(os.path.dirname(os.getcwd())) + "/Snapshot"
    dirPath = 'G:'
    dirPath = dirPath + "/" + institutionID + "/" + studyInstanceUID + "/" + modeName + "/" + instanceName + "/" + sourceName + "/" + userID + "/"

    if (not os.path.exists(dirPath)):
        os.makedirs(dirPath)

    filePath = dirPath + "SnapShotList.json"

    if (not os.path.exists(filePath)):
        print("not exist: " + functionName)
        snapshotResult = []
        functionNameData = {"functionName": functionName}
        snapshotResult.append(functionNameData)
        dataBuffer = {"userID": userID, "userName": userName, "snapshotDateTime": time1_str, "snapshotID": "1","snapshotResult": snapshotResult}
        f = open(filePath, 'w+', encoding='UTF-8')
        DataDest = json.dumps(dataBuffer, ensure_ascii=False)
        t = f.write(DataDest)
        f.close()
    else:
        print("exist: " + functionName)
        f = open(filePath, 'r', encoding='UTF-8')
        FileData = f.read()
        DataJson = json.loads(FileData)
        DataJson["snapshotDateTime"] = time1_str
        #if (DataJson.has_key("snapshotResult")):
        if "snapshotResult" in DataJson:
            snapshotResult = DataJson["snapshotResult"]
            snapshotResultList = []
            FunNameList = []
            for fun in snapshotResult:
                name = fun["functionName"]
                funName = {"functionName": str(name)}
                snapshotResultList.append(funName)
                FunNameList.append(str(name))


            if functionName in FunNameList:
                print("has functionName")
                f = open(filePath, 'w+', encoding='UTF-8')
                DataDest= json.dumps(DataJson, ensure_ascii=False)
                t = f.write(DataDest)
                f.close()
            else:
                functionNameNew = {"functionName": functionName}
                snapshotResultList.append(functionNameNew)
                print("snapshotResultList:",snapshotResultList)
                dataBuffer = {"userID": userID, "userName": userName, "snapshotDateTime": time1_str, "snapshotID": "1", "snapshotResult": snapshotResultList}
                f = open(filePath, 'w+', encoding='UTF-8')
                DataDest= json.dumps(dataBuffer, ensure_ascii=False)
                t = f.write(DataDest)
                f.close()





