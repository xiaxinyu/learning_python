'''
Created on 2018.1.23

@author: summer.xia
@contact: summer_west2010@126.com
'''
import os
import json
import codecs
from account.helper.StringHelper import textSeparator

class ConsumptionAnalyzer(object):
    encoding = 'utf-8'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.path.sep + 'static' + os.path.sep
    ctPath = os.path.join(BASE_DIR, 'consumption-type.json')
    
    def __init__(self):
        self.ctData = self.listConsumptionType(self.ctPath)
        
    def readDictionaryData(self, path):
        with codecs.open(path, 'r', self.encoding) as json_file:
            data = json.load(json_file)
        return data
    
    def listConsumptionType(self, path):
        data = self.readDictionaryData(path)
        rowData = None
        allData = []
        for firstNode in data:
            allData = allData + firstNode['children']
            for secondNode in firstNode['children'] :
                if secondNode.get('default') is not None:
                    if secondNode['default']:
                        rowData = secondNode
                        break
        return {'default':rowData, 'rows':allData}
    
    def getDefaultConsumption(self, data):
        result = data['default']        
        if result is not None:
            result['keyword'] = result['name']
        return result
            
    def getPointedConsumption(self, keyWord, rows):
        result = None
        for row in rows:            
            if keyWord in row['name']:
                result = row
                break
        return result
    
    def getConsumptionByKeyWord(self, text, data):
        result = None
        for row in data['rows']:
            if row.get('keyWords') is None:
                continue
            matchFlag = False
            for keyWord in row['keyWords']:
                if keyWord in text:
                    result = row
                    result['keyword'] = keyWord
                    matchFlag = True
                    break
            if matchFlag:
                break
        return result
    
    def getTransferType(self, text):
        if text:
            if '支付宝-' not in text:
                return False
            if len(text) == 6 or len(text) == 7:
                return True
        return False
    
    def getRentType(self, text, money):
        new_money = int(float(money))
        if  new_money == 3200 or new_money == 3500:
            if '王正根' in text or '聂凤琼' in text:
                return True
            if '微信转账' in text and '消费' in text:
                return True
            if '财付通' in text and '消费' in text:
                return True
        return False
    
    def getWishType(self, text, money):
        if float(money) == 205.13:
            if '支付宝(中国)网络技术有限公@@@@@@消费' in text:
                return True
        return False 
    
    def getConsumptionType(self, text, money):
        defaultConsumption = self.getDefaultConsumption(self.ctData)
        transferConsumption = self.getPointedConsumption('转账', self.ctData['rows'])
        rentConsumption = self.getPointedConsumption('房租', self.ctData['rows'])
        wishConsumption = self.getPointedConsumption('心愿储蓄', self.ctData['rows'])
        
        result = None
        flag = self.getRentType(text, money)
        if flag is True:
            result = rentConsumption
            result['keyword'] = text
            return result
        flag = self.getWishType(text, money)
        if flag is True:
            result = wishConsumption
            result['keyword'] = text
            return result
        flag = self.getTransferType(text)
        if flag is True:
            result = transferConsumption
            result['keyword'] = text
            return result
        
        result = self.getConsumptionByKeyWord(text, self.ctData)
        
        if result is None:
            result = defaultConsumption
            result['keyword'] = 'None'
        return result