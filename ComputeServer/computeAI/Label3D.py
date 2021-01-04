
import json
import os
import time
from django.http import HttpResponse

data_root_path = "H:/ComputeServerData/3DLabel/"


def SubmitLesionsMarkResult(request):
    print("SubmitLesionsMarkResult"+"-"*10)
    if request.method == "POST":
        json_post_data = json.loads(request.body.decode('utf-8'))  # utf-8
        user_id = json_post_data["userID"]
        study_instance_uid = json_post_data["studyInstanceUID"]

        user_data_path = data_root_path+study_instance_uid+'/'+user_id
        if not os.path.exists(user_data_path):
            os.makedirs(user_data_path)

        time_str = str(int(time.time()))
        file_path = user_data_path + '/' + time_str + ".json"

        f = open(file_path, 'w', encoding='UTF-8')
        post_data = json.dumps(json_post_data, ensure_ascii=False)
        f.write(post_data)
        f.close()

        rtn_json_data = {"resultCode": "0", "resultMsg": "保存成功", "isSuccess": True}
        rtn_data = json.dumps(rtn_json_data, ensure_ascii=False)
        return HttpResponse(rtn_data)


def ReturnFailedData():
    rtn_json_data = {"resultCode": "-1", "resultMsg": "失败", "isSuccess": False}
    rtn_data = json.dumps(rtn_json_data, ensure_ascii=False)
    return HttpResponse(rtn_data)


def GetLesionsMarkResult(request):
    print("GetLesionsMarkResult" + "-" * 10)
    if request.method == "POST":
        is_dir = os.path.isdir(data_root_path)  # 判断是否是文件夹
        if not is_dir:  # 不是文件夹直接返回
            print(f"{data_root_path} not a dir")
            return ReturnFailedData()

        res_make_arr = []
        json_post_data = json.loads(request.body.decode('utf-8'))  # utf-8
        study_instance_uid = json_post_data["studyInstanceUID"]
        study_list_dir = os.listdir(data_root_path)  # 获取目录名列表
        if study_instance_uid not in study_list_dir:
            return ReturnFailedData()

        study_root_path = data_root_path+study_instance_uid+'/'
        user_list_dir = os.listdir(study_root_path)
        for user_dir in user_list_dir:  # 遍历根目录
            user_full_dir = (study_root_path+user_dir)
            if os.path.isdir(user_full_dir):  # 是否是文件夹
                user_file_list = os.listdir(user_full_dir)
                for user_file in user_file_list:
                    user_full_file_path = (user_full_dir + '/' + user_file)
                    if os.path.isfile(user_full_file_path):
                        print(user_full_file_path)
                        f = open(user_full_file_path, 'r', encoding='UTF-8')
                        file_data = f.read()
                        f.close()
                        file_json_data = json.loads(file_data)
                        now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                        file_json_data['markDateTime'] = now_str
                        res_make_arr.append(file_json_data)

        result_data = {"resultCode": "0", "isSuccess": True, "resultMsg": "获取成功", "markResult": res_make_arr}
        rtn_data = json.dumps(result_data, ensure_ascii=False)
        return HttpResponse(rtn_data)

