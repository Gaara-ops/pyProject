#coding: UTF-8
from django.conf.urls import url
#from django.contrib import admin
from django.http import HttpResponse
import json
import os
import struct
import sys
import datetime
import platform
import io

def SubmitUserPersonalData(request):
    print("SubmitUserPersonalData")
    if request.method == "POST":
        contentLength = sys.getsizeof(request.body) - 16  # len.
        contentLengthttt = len(request.body) - 16  # len
        #print("contentLength:" + str(contentLength) + "contentLengthttt:" + str(contentLengthttt))
        strUnpack = "<qq{}s".format(str(contentLengthttt))
        #print("strUnpack:" + strUnpack)
        dataLength, headerLength, content = struct.unpack(strUnpack, request.body)
        print("dataLength:" + str(dataLength))
        print("headerLength:" + str(headerLength))
        # print("content:" + str(content))

        # 解析头和数据
        bodyLength = contentLengthttt - headerLength
        contentHeader, contentBody = struct.unpack("<{}s{}s".format(str(headerLength), str(bodyLength)), content)

        JsonBuffer = json.loads(contentHeader.decode('utf-8'))  # utf-8
        Meta = JsonBuffer["Meta"]
        #dirPath = os.path.abspath(os.path.dirname(os.getcwd())) + "/UserPersonalData"
        dirPath = 'G:'
        unpackParam = ""
        countData = 0
        for info in Meta:
            DataSize = info["DataSize"]
            TextSize = info["TextSize"]
            print("DataSize:" + str(DataSize) + "  " + str(TextSize))
            countData = countData + 1
            unpackParam = unpackParam + "{}s{}s".format(str(TextSize), str(DataSize))

        unpackParam = "<" + unpackParam
        #print("unpackParam:" + str(unpackParam))
        streamData = []
        streamData = struct.unpack(unpackParam, contentBody)

        count = 0
        storeDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for info in Meta:
            # print("info:" + str(info))
            DataSize = info["DataSize"]
            TextSize = info["TextSize"]
            Type = info["Type"]
            print("DataSize:" + str(DataSize) + "  " + str(TextSize))
            if int(TextSize) > 0:
                TextContent = streamData[2 * count]
                BodyContent = streamData[2 * count + 1]

                # TextContent, BodyContent = struct.unpack("<{}s{}s".format(str(TextSize),str(DataSize)), contentBody)
                try:
                    mataInfo = json.loads(TextContent.decode('utf-8'))  # 'gbk'
                except Exception as e:
                    print("Exception: ", e)

                # print("mataInfo:" + str(mataInfo))
                institutionID = mataInfo["institutionID"]
                userID = mataInfo["userID"]
                userName = mataInfo["userName"]
                typeID = mataInfo["typeID"]
                function = mataInfo["function"]
                fileName = mataInfo["fileName"]
                if institutionID == '':
                    institutionID = '100000'
                if userID == '':
                    userID = '88'
                if userName == '':
                    userName = 'wg0'

                SetUserPersonalDataList(institutionID, userID, userName, function, fileName, storeDateTime, typeID)

                filePath = dirPath + "/" + institutionID + "/" + userID + "/" + userName + "/" + function + "/" + typeID + "/"
                if not os.path.exists(filePath):
                    os.makedirs(filePath)
                filePath = filePath + fileName
                print("filePath:" + filePath)
                if typeID == "1":
                    if "imagesData" in mataInfo:
                        imagesData = mataInfo["imagesData"]
                        f = io.open(filePath, 'w+', encoding='UTF-8')
                        t = json.dumps(imagesData, ensure_ascii=False)
                        t = f.write(t)
                        f.close()
                else:
                    f = io.open(filePath, 'wb')
                    t = f.write(BodyContent)
                    f.close()
            count = count + 1

        rtnJson = {"resultCode": "0", "isSuccess": True, "resultMsg": "0"}
        t = json.dumps(rtnJson, ensure_ascii=False)
        return HttpResponse(t)
    else:
        rtnJson = {"resultCode": "-1", "isSuccess": False, "resultMsg": "获取失败", "jsonData": ""}
        t = json.dumps(rtnJson, ensure_ascii=False)
        return HttpResponse(t)


def SetUserPersonalDataList(institutionID, userID, userName, function, fileName, storeDateTime, typeID):
    print("SetUserPersonalDataList:")
    #dirPath = os.path.abspath(os.path.dirname(os.getcwd())) + "/UserPersonalData"
    dirPath = 'G:'
    dirPath = dirPath + "/" + institutionID + "/" + userID + "/" + userName + "/" + function + "/"

    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

    filePath = dirPath + "UserPersonalDataList.json"

    if not os.path.exists(filePath):
        print("not exist: " + filePath)
        jsonData = []
        dataBuffer = {"userID": userID, "userName": userName, "storeDateTime": storeDateTime, "fileName": fileName, "typeID": typeID}
        jsonData.append(dataBuffer)
        f = io.open(filePath, 'w+', encoding='UTF-8')
        DataDest = json.dumps(jsonData, ensure_ascii=False)
        t = f.write(DataDest)
        f.close()
    else:
        print("exist: " + filePath)
        f = io.open(filePath, 'r', encoding='UTF-8')
        FileData = f.read()
        DataJson = json.loads(FileData)
        fileNameList = []
        jsonData = []
        for info in DataJson:
            typeIDTmp = info["typeID"]
            fileNameTmp = info["fileName"]
            fileNameList.append(fileNameTmp)
            userIDTmp = info["userID"]
            userNameTmp = info["userName"]
            storeDateTimeTmp = info["storeDateTime"]
            dataBuffer = {"userID": userIDTmp, "userName": userNameTmp, "storeDateTime": storeDateTimeTmp, "fileName": fileNameTmp, "typeID": typeIDTmp}
            jsonData.append(dataBuffer)

        if fileName in fileNameList:
            print("fileName exist" + fileName)
        else:
            dataBuffer = {"userID": userID, "userName": userName, "storeDateTime": storeDateTime, "fileName": fileName, "typeID": typeID}
            jsonData.append(dataBuffer)
            f = io.open(filePath, 'w+', encoding='UTF-8')
            DataDest = json.dumps(jsonData, ensure_ascii=False)
            t = f.write(DataDest)
            f.close()



def GetUserPersonalDataList(request):
    print("GetUserPersonalDataList Begin")
    if request.method == "POST":
        JsonBuffer = json.loads(request.body.decode('utf-8'))  # utf-8 gbk
        JsonDict = {}
        JsonDict = JsonBuffer
        typeID = ""
        hasTypeID = False
        if "typeID" in JsonDict:
            typeID = JsonBuffer["typeID"]
            hasTypeID = True
        institutionID = JsonBuffer["institutionID"]
        userID = JsonBuffer["userID"]
        userName = JsonBuffer["userName"]
        function = JsonBuffer["function"]
        if institutionID == '':
            institutionID = '100000'
        if userID == '':
            userID = '88'
        if userName == '':
            userName = 'wg0'

        #dirPath = os.path.abspath(os.path.dirname(os.getcwd())) + "/UserPersonalData"
        dirPath = 'G:'
        filePath = dirPath + "/" + institutionID + "/" + userID + "/" + userName + "/" + function + "/" + "UserPersonalDataList.json"
        print("GetUserPersonalDataList" + filePath)
        if (os.path.exists(filePath)):
            f = io.open(filePath, 'r', encoding='UTF-8')
            FileData = f.read()
            FileJsonData = json.loads(FileData)
            DataJson = json.loads(FileData)

            jsonData = []
            for info in DataJson:
                if hasTypeID:
                    typeIDTmp = info["typeID"]
                    if typeIDTmp == typeID:
                        fileNameTmp = info["fileName"]
                        userIDTmp = info["userID"]
                        userNameTmp = info["userName"]
                        storeDateTimeTmp = info["storeDateTime"]
                        dataBuffer = {"userID": userIDTmp, "userName": userNameTmp, "storeDateTime": storeDateTimeTmp,
                                      "fileName": fileNameTmp}
                        jsonData.append(dataBuffer)
                else:
                    fileNameTmp = info["fileName"]
                    userIDTmp = info["userID"]
                    userNameTmp = info["userName"]
                    storeDateTimeTmp = info["storeDateTime"]
                    dataBuffer = {"userID": userIDTmp, "userName": userNameTmp, "storeDateTime": storeDateTimeTmp,
                                  "fileName": fileNameTmp}
                    jsonData.append(dataBuffer)

            rtnJson = {"resultCode": "0", "isSuccess": True, "resultMsg": "0", "jsonData": jsonData}
            t = json.dumps(rtnJson, ensure_ascii=False)
            f.close()
            print("GetUserPersonalDataList End")
            return HttpResponse(t)
        else:
            rtnJson = {"resultCode": "-1", "isSuccess": False, "resultMsg": "GetUserPersonalDataList失败", "jsonData": ""}
            t = json.dumps(rtnJson, ensure_ascii=False)
            print("GetUserPersonalDataList End")
            return HttpResponse(t)

def GetUserPersonalData(request):
    print("GetUserPersonalData Begin")
    if request.method == "POST":
        JsonBuffer = json.loads(request.body.decode('utf-8'))  # utf-8 gbk
        institutionID = JsonBuffer["institutionID"]
        userID = JsonBuffer["userID"]
        userName = JsonBuffer["userName"]
        typeID = JsonBuffer["typeID"]
        function = JsonBuffer["function"]
        fileName = JsonBuffer["fileName"]

        print("institutionID:" + institutionID)
        print("userID:" + userID)
        print("typeID:" + typeID)
        print("function:" + function)
        print("fileName:" + fileName)
        #dirPath = os.path.abspath(os.path.dirname(os.getcwd())) + "/UserPersonalData"
        dirPath = 'G:'
        filePath = dirPath + "/" + institutionID + "/" + userID + "/" + userName + "/" + function + "/" + typeID + "/"
        if not os.path.exists(filePath):
            os.makedirs(filePath)

        filePath = filePath + fileName
        print("FilePath:" + filePath)
        if typeID == "1":
            if os.path.exists(filePath):
                f = io.open(filePath, 'r', encoding='UTF-8')
                userpersonaldata = f.read()
                jsonData = []
                dataBuffer = {"dataBuffer": userpersonaldata}
                jsonData.append(dataBuffer)
                rtnJson = {"resultCode": "0", "isSuccess": True, "resultMsg": "GetUserPersonalData succ", "jsonData": jsonData}
                t = json.dumps(rtnJson, ensure_ascii=False)
                f.close()
                return HttpResponse(t)
            else:
                rtnJson = {"resultCode": "-1", "isSuccess": False, "resultMsg": "GetUserPersonalData fail1", "jsonData": ""}
                t = json.dumps(rtnJson, ensure_ascii=False)
                return HttpResponse(t)
        else:
            print("POST RAW")
            if os.path.exists(filePath):
                f = io.open(filePath, 'rb')
                t = f.read()
                f.close()
                print("GetUserPersonalData End")
                return HttpResponse(t)
            else:
                rtnJson = {"resultCode": "-1", "isSuccess": False, "resultMsg": "GetUserPersonalData fail2", "jsonData": ""}
                t = json.dumps(rtnJson, ensure_ascii=False)
                print("GetUserPersonalData End")
                return HttpResponse(t)
    else:
        rtnJson = {"resultCode": "-1", "isSuccess": False, "resultMsg": "GetUserPersonalData fail3", "jsonData": ""}
        t = json.dumps(rtnJson, ensure_ascii=False)
        print("GetUserPersonalData End")
        return HttpResponse(t)

def DeleteUserPersonalData(request):
    print("DeleteUserPersonalData Begin")
    #print("request.body={}".format(request.body))
    if request.method == "POST":
        JsonBuffer = json.loads(request.body.decode('utf-8'))  # utf-8
        JsonDict = {}
        JsonDict = JsonBuffer
        institutionID = JsonBuffer["institutionID"]
        userID = JsonBuffer["userID"]
        userName = JsonBuffer["userName"]
        typeID = ""
        fileName = ""
        hastypeID = False
        hasFileName = False
        if "typeID" in JsonDict:
            typeID = JsonBuffer["typeID"]
            if typeID != "":
                hastypeID = True
        function = JsonBuffer["function"]
        if "fileName" in JsonDict:
            fileName = JsonBuffer["fileName"]
            if fileName != "":
                hasFileName = True

        dirPath = os.path.abspath(os.path.dirname(os.getcwd())) + "/UserPersonalData"

        bDir = False
        listPath =[]
        if not hastypeID:
            if not hasFileName:
                filePath = dirPath + "/" + institutionID + "/" + userID + "/" + userName + "/" + function
                bDir = True
                listPath.append(filePath)
            else:
                filePath = dirPath + "/" + institutionID + "/" + userID + "/" + userName + "/" + function + "/1/" + fileName
                listPath.append(filePath)
                filePath = dirPath + "/" + institutionID + "/" + userID + "/" + userName + "/" + function + "/2/" + fileName
                listPath.append(filePath)
        else:
            if not hasFileName:
                filePath = dirPath + "/" + institutionID + "/" + userID + "/" + userName + "/" + function + "/" + typeID
                bDir = True
                listPath.append(filePath)
            else:
                filePath = dirPath + "/" + institutionID + "/" + userID + "/" + userName + "/" + function + "/" + typeID + "/" + fileName
                listPath.append(filePath)

        listfilePath = dirPath + "/" + institutionID + "/" + userID + "/" + userName + "/" + function + "/" + "UserPersonalDataList.json"
        for path in listPath:
            if os.path.exists(path):
                if bDir:
                    print("remove dir")
                    #os.rmdir(path)
                    shutil.rmtree(path)
                    #os.remove(listfilePath)
                else:
                    print("remove file")
                    os.remove(path)
                    #####修改list内容
        print("DeleteUserPersonalData DataList" + listfilePath)
        if os.path.exists(listfilePath):
            f = io.open(listfilePath, 'r', encoding='UTF-8')
            FileData = f.read()
            DataJson = json.loads(FileData)
            jsonData = []
            for info in DataJson:
                typeIDTmp = info["typeID"]
                fileNameTmp = info["fileName"]
                userIDTmp = info["userID"]
                userNameTmp = info["userName"]
                storeDateTimeTmp = info["storeDateTime"]
                print("fileNameTmp" + fileNameTmp + fileName)
                print("typeIDTmp" + typeIDTmp + typeID)
                if (hastypeID and typeIDTmp != typeID) \
                        or (hasFileName and fileNameTmp != fileName):
                        dataBuffer = {"userID": userIDTmp, "userName": userNameTmp,
                                      "storeDateTime": storeDateTimeTmp, "fileName": fileNameTmp,
                                      "typeID": typeIDTmp}
                        jsonData.append(dataBuffer)

            f = io.open(listfilePath, 'w+', encoding='UTF-8')
            DataDest = json.dumps(jsonData, ensure_ascii=False)
            t = f.write(DataDest)
            f.close()

            rtnJson = {"resultCode": "0", "isSuccess": True, "resultMsg": "DeleteUserPersonalData succ"}
            t = json.dumps(rtnJson, ensure_ascii=False)
            print("DeleteUserPersonalData End")
            return HttpResponse(t)
        else:
            rtnJson = {"resultCode": "-1", "isSuccess": False, "resultMsg": "GetUserPersonalData fail"}
            t = json.dumps(rtnJson, ensure_ascii=False)
            print("DeleteUserPersonalData End")
            return HttpResponse(t)