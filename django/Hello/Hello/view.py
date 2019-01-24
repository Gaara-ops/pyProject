from django.http import HttpResponse
from django.http import JsonResponse
import json

def writeToFile(strdata):
	outfilepath = 'aiInfo.json'
	with open(outfilepath,'w') as saveFile:#写入数据到文件
		saveFile.write(strdata)

def ParseJson(jsonstr):
	json_ai = {}
	json_ai["dataBuffer"] = jsonstr
	json_ai["userID"] = "159357"
	json_ai["aiDateTime"] = "20190123"
	json_result = {}
	json_result["aiResult"] = json_ai
	json_result["isSuccess"] = 1
	json_result["resultCode"] = "0"
	json_result["resultMsg"] = "success"
	writeToFile(json.dumps(json_result))
	
	
#json->string  json.dumps(allSaveData)
#bytes->string str(request.body,'utf-8')
#string->json json.loads(str)
def GetUserAIInfo(request):
	f = open("aiInfo.json",encoding='UTF-8')
	j = json.load(f)
    #return HttpResponse(json.dumps(j.get("GET")))
	return JsonResponse(j)
def SaveUserAIInfo(request):
	jsonstr = (str(request.body,'utf-8'))
	ParseJson(jsonstr)
	json_res = {}
	json_res["bIsSuccess"] = 1
	json_res["strResultCode"] = "0"
	return JsonResponse(json_res)

def DownLoadAIFeedBack(request):
	f = open("aiFeedBack.json",encoding='UTF-8')
	j = json.load(f)
	return JsonResponse(j)
	