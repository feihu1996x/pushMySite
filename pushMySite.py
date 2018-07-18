#!/usr/bin/python3

"""
@file: pushMySite.py
@brief: push my site(feihu1996.cn) to baidu search engine.
@author: feihu1996.cn
@date: 18-05-05
@version: 1.0
"""

import logging
import os
import re
import subprocess
from urllib.request import urlopen


from lxml import etree


class PushMySite:
    def __init__(self):
        self.targetUrl = 'http://www.feihu1996.cn/'
        self.totalPageNumPattern = re.compile('<a.*?href=.*?http://www\.feihu1996\.cn/\?page=(\d{1,}).*?class=.*?c-nav ease.*?title=.*?>末页.*?</a>')
        self.articleUrlPattern = re.compile('http://www\.feihu1996\.cn/\?id=\d{1,}')

        self.articleUrls = set()
        
        logging.basicConfig(filename='pushmysite.log', level=logging.INFO, format='%(asctime)s-%(levelname)s-%(message)s')


    def start(self):
        '''
        push my site(feihu1996.cn) to baidu search engine.
        '''

        # get index data
        indexData = urlopen(self.targetUrl).read().decode('utf-8')

        # get total page num
        totalPageNum = int(self.totalPageNumPattern.findall(indexData)[0])

        # get all article url by traversal
        for currentPageNum in range(1, totalPageNum+1):
          currentPageData = urlopen(self.targetUrl + '?' + 'page=' + str(currentPageNum)).read().decode("utf-8")
          currentPageArticleUrls = set(self.articleUrlPattern.findall(currentPageData))
          for currentPageArticleUrl in currentPageArticleUrls:
              self.articleUrls.add(currentPageArticleUrl)    
       
        # write all article url into text file
        tempFile = open('temp', 'wb')
        for articleUrl in self.articleUrls:
          tempFile.write(articleUrl.encode('utf-8'))
          tempFile.write('\n'.encode('utf-8'))
        tempFile.close()
 
        # push site to baidu search engine
        pushMySiteShell = subprocess.Popen(args='''curl -H 'Content-Type:text/plain' --data-binary @temp "http://data.zz.baidu.com/urls?site=www.feihu1996.cn&token=ZVYgja02dMgiC0AN"''', shell=True, stdout=subprocess.PIPE)
        pushMySiteShell.wait()
        result = pushMySiteShell.stdout.read()
        result = str(result)
        result = re.sub('b|\'', '', result)
        os.remove("temp")
        
        logging.info(result)

        return result


if __name__ == '__main__':
    result = PushMySite().start()
    print(result)

