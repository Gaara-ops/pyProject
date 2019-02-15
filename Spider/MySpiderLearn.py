# -*- coding:UTF-8 -*-
import requests, sys
from bs4 import BeautifulSoup

class downloader(object):
    def __init__(self):
        self.server = 'http://www.biqukan.com'
        self.target = 'http://www.biqukan.com/1_1094'
        self.names = []
        self.urls = []
        self.nums = 0
        self.fileptr = open('one_forever.txt','a',encoding='utf-8')

    def get_download_url(self):
        req = requests.get(url = self.target)
        html = req.text
        div_bf = BeautifulSoup(html,'html.parser')
        div = div_bf.find_all('div',class_ = 'listmain')
        a_bf = BeautifulSoup(str(div[0]),'html.parser')
        a = a_bf.find_all('a')
        self.nums = len(a[15:])
        for each in a[15:]:
            self.names.append(each.string)
            self.urls.append(self.server+each.get('href'))

    def get_contents(self,target):
        req = requests.get(url=target)
        html = req.text
        bf = BeautifulSoup(html,'html.parser')
        texts = bf.find_all('div',class_='showtxt')
        print("get_contents:",len(texts))
        if(len(texts)):
            texts = texts[0].text
            return texts
        else:
            print(html)
        return ''

    def writer(self,name,path,text):
        self.fileptr.write(name + '\n')
        self.fileptr.writelines(text)
        self.fileptr.write('\n\n')

if __name__ == '__main__':
    dl = downloader()
    dl.get_download_url()
    print('begin download')
    '''
    print(dl.nums)
    print(len(dl.names))
    print(len(dl.urls))
    '''
    for i in range(1,50):
        print(dl.names[i] , dl.urls[i])
        dl.writer(dl.names[i],'one_forever.txt',dl.get_contents(dl.urls[i]))
        sys.stdout.write(" had download:%.3f" % float(i/dl.nums)+'\r')
        sys.stdout.flush()

    print('<<one forver>> had download all')

