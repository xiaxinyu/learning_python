'''
Created on 2018.1.12

@author: summer.xia
@contact: summer_west2010@126.com
'''
import datetime

def isNotEmpty(charactor):   
    return charactor and len(charactor.strip()) > 0

def parseDate(strDate):
    return datetime.datetime.strptime(strDate, "%Y%m%d")

def formatDateTime(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")