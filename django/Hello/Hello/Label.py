#coding: UTF-8
from django.conf.urls import url
#from django.contrib import admin
from django.http import HttpResponse
import json
import os
import struct
import sys
import datetime


def TestSaveChineseLanguage(request):
    print("TestSaveChineseLanguage")
    if request.method == "POST":
        jsonBuffer = json.loads(request.body.decode('utf-8'))
        userId = jsonBuffer["userId"]
        userName = jsonBuffer["userName"]
        
        dirPath = "E:/pywork/pyProject/django/Hello/Label"

        if (not os.path.exists(dirPath)):
            os.makedirs(dirPath)
        filePath = dirPath + "/" + userId +".json"

        f = open(filePath, 'w+', encoding='UTF-8')
        t = json.dumps(jsonBuffer, ensure_ascii=False)
        t = f.write(t)
        f.close()
        
        rtnJson = {"resultCode": "0", "resultMsg": "保存成功", "isSuccess": True}
        t1 = json.dumps(rtnJson, ensure_ascii=False)
        return HttpResponse(t1)
def TestGetChineseLanguage(request):
    print("TestGetChineseLanguage")
    if request.method == "POST":
        jsonBuffer = json.loads(request.body.decode('utf-8'))
        userId = jsonBuffer["userId"]
        userName = jsonBuffer["userName"]
        
        dirPath = "E:/pywork/pyProject/django/Hello/Label"

        if (not os.path.exists(dirPath)):
            os.makedirs(dirPath)
        filePath = dirPath + "/" + userId +".json"

        f = open(filePath, 'r', encoding='UTF-8')
        fileData = f.read()
        fileJsonData = json.loads(fileData)
        f.close()
        
        rtnJson = {"resultCode": "0", "resultMsg": "保存成功", "isSuccess": True,"resultData": fileJsonData}
        t1 = json.dumps(rtnJson, ensure_ascii=False)
        return HttpResponse(t1)
def SubmitLesionsMarkResult(request):
    #print("request.body={}".format(request.body))

    print("SubmitLesionsMarkResult")
    if request.method == "POST":
        JsonBuffer = json.loads(request.body.decode('utf-8'))  # utf-8
        institutionID = JsonBuffer["institutionID"]
        userID = JsonBuffer["userID"]
        userName = JsonBuffer["userName"]
        #patientID = JsonBuffer["patientID"]
        #patientName = JsonBuffer["patientName"]
        #studyID = JsonBuffer["studyID"]
        #accessionNumber = JsonBuffer["accessionNumber"]
        studyInstanceUID = JsonBuffer["studyInstanceUID"]
        projectID = JsonBuffer["projectID"]
        topicID = JsonBuffer["topicID"]
        researchID = JsonBuffer["researchID"]
        markAuthority = JsonBuffer["markAuthority"]
        #markInfo = JsonBuffer["markInfo"]
        pathologys = JsonBuffer["pathologys"]
        dataBuffer = JsonBuffer["dataBuffer"]
        imagePath = JsonBuffer["imagePath"]
        typeID = JsonBuffer["typeID"]

        dirPath = "E:/pywork/pyProject/django/Hello/Label"

        if (not os.path.exists(dirPath)):
            os.makedirs(dirPath)
        filePath = dirPath + "/" + userID +".json"

        f = open(filePath, 'w+', encoding='UTF-8')
        t = json.dumps(JsonBuffer, ensure_ascii=False)
        t = f.write(t)
        f.close()

        rtnJson = {"resultCode": "0", "resultMsg": "保存成功", "isSuccess": True}
        t1 = json.dumps(rtnJson, ensure_ascii=False)
        return HttpResponse(t1)

def GetLesionsMarkResult(request):
    # print("request.body={}".format(request.body))
    print("GetLesionsMarkResult")
    if request.method == "POST":
        JsonBuffer = json.loads(request.body.decode('utf-8'))  # utf-8
        institutionID = JsonBuffer["institutionID"]
        userID = JsonBuffer["userID"]
        userName = JsonBuffer["userName"]
        #patientID = JsonBuffer["patientID"]
        #patientName = JsonBuffer["patientName"]
        #studyID = JsonBuffer["studyID"]
        #accessionNumber = JsonBuffer["accessionNumber"]
        studyInstanceUID = JsonBuffer["studyInstanceUID"]
        projectID = JsonBuffer["projectID"]
        topicID = JsonBuffer["topicID"]
        researchID = JsonBuffer["researchID"]
        markAuthority = JsonBuffer["markAuthority"]
        #markInfo = JsonBuffer["markInfo"]
        imagePath = JsonBuffer["imagePath"]
        typeID = JsonBuffer["typeID"]

        dirPath = "E:/pywork/pyProject/django/Hello/Label"

        markResult = []
        for root, dirs, files in os.walk(dirPath):
            # 遍历文件
            for f in files:
                filePath = os.path.join(root, f)
                print("filePath " + filePath)
                if (os.path.exists(filePath)):
                    f = open(filePath, 'r', encoding='UTF-8')
                    FileData = f.read()
                    FileJsonData = json.loads(FileData)

                    userID1 = FileJsonData["userID"]
                    userName1 = FileJsonData["userName"]
                    projectID1 = FileJsonData["projectID"]
                    topicID1 = FileJsonData["topicID"]
                    researchID1 = FileJsonData["researchID"]
                    markAuthority1 = FileJsonData["markAuthority"]
                    dataBuffer1 = FileJsonData["dataBuffer"]
                    #data = {"markDateTime": markDateTime}
                    data = {"userID": userID1, "userName": userName1, "projectID": projectID1, "topicID": topicID1,
                            "researchID": researchID1, "markAuthority": markAuthority1,"markDateTime": "2020-07-20", "dataBuffer": dataBuffer1}

                    markResult.append(data)

                else:
                    rtnJson = {"resultCode": "-1", "resultMsg": "获取失败", "resultData": "", "isSuccess": False}
                    t = json.dumps(rtnJson, ensure_ascii=False)
                    return HttpResponse(t)


        resultData = {"resultCode": "0", "isSuccess": True, "resultMsg": "获取成功",
                      "markResult": markResult}

        t = json.dumps(resultData, ensure_ascii=False)

        f.close()
        return HttpResponse(t)