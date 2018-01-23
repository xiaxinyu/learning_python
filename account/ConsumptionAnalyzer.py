'''
Created on 2018.1.23

@author: summer.xia
@contact: summer_west2010@126.com
'''
import os
import json
import codecs


class ConsumptionAnalyzer(object):
    encoding = 'utf-8'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.path.sep + 'account' + os.path.sep + 'static' + os.path.sep
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
    
    def getConsumptionByTransfer(self, text, transferConsumption):
        result = None
        if '支付宝-' not in text:
            return result
        if len(text) == 6 or len(text) == 7:
            result = transferConsumption            
            result['keyword'] = text
        return result
    
    def getConsumptionType(self, text):
        defaultConsumption = self.getDefaultConsumption(self.ctData)
        transferConsumption = self.getPointedConsumption('转出', self.ctData['rows'])
        
        result = self.getConsumptionByKeyWord(text, self.ctData)
        if result is None:
            result = self.getConsumptionByTransfer(text, transferConsumption)
        
        if result is None:
            result = defaultConsumption
        return result
