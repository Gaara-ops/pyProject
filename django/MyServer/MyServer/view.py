from django.http import HttpResponse
from django.http import JsonResponse
import json
 
def hello(request):
    return HttpResponse("Hello world ! ")

def DownLoadAIFeedBack(request):
	f = open("aiFeedBack.json",encoding='UTF-8')
	j = json.load(f)
	return JsonResponse(j)