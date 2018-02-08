'''
Created on 2018.1.12

@author: summer.xia
@contact: summer_west2010@126.com
'''
import datetime
import uuid

textSeparator='@@'

def isNotEmpty(charactor):   
    return charactor and len(charactor.strip()) > 0

def parseDate(strDate, fmt='%Y%m%d'):
    return datetime.datetime.strptime(strDate, fmt)

def parseDateTime(strDate, fmt='%Y%m%d%H:%M:%S'):
    return datetime.datetime.strptime(strDate, fmt)

def formatDateTime(date, fmt='%Y-%m-%d %H:%M:%S'):
    return date.strftime(fmt)

def getUUID():
    return uuid.uuid1()