import requests

#执行API调用并存储响应
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
r = requests.get(url)
print("Status code:",r.status_code)
#将API响应存储在一个变量中
response_dict = r.json()
#搜索有关仓库的信息
repo_dicts = response_dict['items']

repo_dict = repo_dicts[0]
for key in sorted(repo_dict.keys()):
    print(key)
