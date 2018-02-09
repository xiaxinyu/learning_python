'''
Created on 2018.1.12

@author: summer.xia
@contact: summer_west2010@126.com
'''
import os
import json
import codecs
from account.analyzer.ConsumptionAnalyzer import ConsumptionAnalyzer


class BusinessAnalyzer(object):
    encoding = 'utf-8'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.path.sep + 'static' + os.path.sep;
    dcPath = os.path.join(BASE_DIR, 'disbursement-channels.json')
    touPath = os.path.join(BASE_DIR, 'type-of-use.json')
    ctPath = os.path.join(BASE_DIR, 'consumption-type.json')
    descriptionColumnIndex = 6
    transactionColumnIndex = 3
    headerRowIndex = 0 
    disbursementNewColumn1 = '支付渠道名称'
    disbursementNewColumn2 = '支付渠道编码' 
    typeOfUseNewColumn1 = '使用类型名称'
    typeOfUseNewColumn2 = '使用类型编码' 
    consumptionNewColumn1 = '消费类型名称'
    consumptionNewColumn2 = '消费类型编码'
    keywordNewColumn1 = '关键字'
    
    def __init__(self, lines=[]):
        self.lines = lines
        self.dcData = self.listOrdinaryType(self.dcPath)
        self.touData = self.listOrdinaryType(self.touPath)
        self.consumptionAnalyzer = ConsumptionAnalyzer()     
        
    def readDictionaryData(self, path):
        with codecs.open(path, 'r', self.encoding) as json_file:
            data = json.load(json_file)
        return data
    
    def listOrdinaryType(self, path):
        data = self.readDictionaryData(path)
        defaultRow = None
        for i, row in enumerate(data):
            if i == 0:
                defaultRow = row
            if row['default']:
                defaultRow = row
                break
        return {'default':defaultRow, 'rows':data}
    
    def getOrdinaryType(self, text, data):
        result = data['default']
        for key in data['rows']:
            if key["name"] in text:
                result = key
        return result
    
    def calculate(self, lines=[]):
        if len(lines) <= 0:
            return None
        for index, line in enumerate(lines):
            if index == self.headerRowIndex:
                line.append(self.disbursementNewColumn1)
                line.append(self.disbursementNewColumn2)
                line.append(self.typeOfUseNewColumn1)
                line.append(self.typeOfUseNewColumn2)
                line.append(self.consumptionNewColumn1)
                line.append(self.consumptionNewColumn2)
                line.append(self.keywordNewColumn1)
                continue
            if line is None:
                continue 
            description = line[self.descriptionColumnIndex]
            dc = self.getOrdinaryType(description, self.dcData)
            line.append(dc['name'])
            line.append(dc['value'])
            tou = self.getOrdinaryType(description, self.touData)
            line.append(tou['name'])
            line.append(tou['value'])
            money = line[self.transactionColumnIndex]
            ct = self.consumptionAnalyzer.getConsumptionType(description, money)
            if ct is not None:
                line.append(ct['name'])
                line.append(ct['value'])
                line.append(ct['keyword'])
        return lines
