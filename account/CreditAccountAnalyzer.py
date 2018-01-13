'''
Created on 2018.1.12

@author: summer.xia
@contact: summer_west2010@126.com
'''
import os
import json
import codecs


class CreditAccountAnalyzer(object):
    encoding = 'utf-8'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dcPath = os.path.join(BASE_DIR, 'account' + os.path.sep + 'static' + os.path.sep + 'disbursement-channels.json')
    touPath = os.path.join(BASE_DIR, 'account' + os.path.sep + 'static' + os.path.sep + 'type-of-use.json')
    ctPath = os.path.join(BASE_DIR, 'account' + os.path.sep + 'static' + os.path.sep + 'consumption-type.json')
    descriptionColumnIndex = 5
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
        self.ctData = self.listConsumptionType(self.ctPath)
        
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
    
    def getOrdinaryType(self, text, data):
        result = data['default']
        for key in data['rows']:
            if key["name"] in text:
                result = key
                break
        return result
    
    def getConsumptionType(self, text, data):
        result = data['default']
        if result is not None:
            result['keyword'] = result['name']
        for row in data['rows']:
            if row.get('keyWords') is None:
                continue
            matchFlag = False
            for keyWord in row['keyWords']:
                if keyWord in text:
                    row['keyword'] = keyWord
                    result = row
                    matchFlag = True
                    break
            if matchFlag:
                break
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
            ct = self.getConsumptionType(description, self.ctData)
            if ct is not None:
                line.append(ct['name'])
                line.append(ct['value'])
                line.append(ct['keyword'])
        return lines

# if __name__ == '__main__':
#     a = CreditAccountAnalyzer()
#     a.listConsumptionType(a.ctPath)
