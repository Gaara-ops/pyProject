# -*- coding:utf-8 -*-

import sys
import nu

from bs4 import BeautifulSoup
import requests
''''''
vtkexample_url = "https://lorensen.github.io/VTKExamples/site/Cxx/"
# get request
res = requests.get(vtkexample_url)
strhtml = res.text
'''
with open('./strexamplehtml.txt','w') as examplevtk:
    examplevtk.write(strhtml)
'''

'''
outfilepath = './test.txt'
strAllData = "";
with open(outfilepath) as pFile:
    strAllData = pFile.read()
'''

exampleFlag = '../Cxx/'
# parse html
soup = BeautifulSoup(strhtml,'html.parser')

real_name = []
all_taga = soup.find_all('a')
print(len(all_taga))
for tag in all_taga:
    if (exampleFlag in tag['href']):
        real_name.append(tag.string)
print(real_name)
print(len(real_name))
with open('./vtk_example_20200804.txt','w') as tmpSave:
    tmpSave.write(str(str(real_name).encode('utf-8')))

print("over\n")

