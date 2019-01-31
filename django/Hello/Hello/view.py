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

def GetDataFromAIStore(request):
	f = open("aiStore.json",encoding='UTF-8')
	j = json.load(f)
	return JsonResponse(j)

filename = "functionlist.json"
def ParseParamInfo(jsonobj):
	global filename
	functionName = jsonobj["functionName"]
	if(functionName == "FunctionList"):
		filename = "functionlist.json"
	elif(functionName == "DataAttribute"):
		filename = "volumeinfo.json"
	elif(functionName == "AD.raw"):
		filename = "paramraw/AD.raw"
	elif(functionName == "AK.raw"):
		filename = "paramraw/AK.raw"
	elif(functionName == "FA.raw"):
		filename = "paramraw/FA.raw"
	elif(functionName == "MD.raw"):
		filename = "paramraw/MD.raw"
	elif(functionName == "MK.raw"):
		filename = "paramraw/MK.raw"
	elif(functionName == "RD.raw"):
		filename = "paramraw/RD.raw"
	elif(functionName == "RK.raw"):
		filename = "paramraw/RK.raw"

def GetFunlistInfo(request):
	jsonstr = (str(request.body,'utf-8'))
	jsonobj = json.loads(jsonstr)
	ParseParamInfo(jsonobj)
	if('.raw' in filename):
		rawData = open(filename,'rb').read()
		return HttpResponse(rawData)
	else:
		f = open(filename,encoding='UTF-8')
		j = json.load(f)
		return JsonResponse(j)