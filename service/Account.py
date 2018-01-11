'''
Created on 2018.1.10

@author: summer.xia
@contact: summer_west2010@126.com
'''
from service.FileHelper import getFiles
from service.FileHelper import getAllLines
from service.FileHelper import generateFile
import os
import json
import codecs

directoryPath = '/Users/summer/Desktop/account'
# directoryPath = 'd:\\test'
encoding = 'utf-8'
filterHeaderKeyWord = '交易明细'
spliter = ' '
filterDataKeyWords = ['CNY/', '人民币/']
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def isNotEmpty(charactor):   
    return charactor and len(charactor.strip()) > 0


def getDataLines(lines):
    if len(lines) < 0:
        return None
    startFlag = False
    dataLines = []
    counter = 0
    for line in lines:
        if startFlag:
            if counter == 0 or counter > 1:
                dataLines.append(line)
            counter = counter + 1
        if filterHeaderKeyWord in line:
            startFlag = True
    return dataLines


def  generateAccountMatrix(lines):
    if len(lines) < 0:
        return None
    matrix = []
    for line in lines:
        array = line.split(spliter)
        cleanArray1 = filter(isNotEmpty, array)
        cleanArray2 = []
        for item in cleanArray1:
            cleanArray2.append(item.strip())
        matrix.append(cleanArray2)
    return matrix

    
def getAllDataLines():
    fileItems = getFiles(directoryPath)
    if not fileItems:
        print('No data files are available')
    texts = {}
    for fileItem in fileItems:
        lines = getAllLines(fileItem.absolutePath, encoding)
        if lines is not None and len(lines) > 0:
            dataLines = generateAccountMatrix(getDataLines(lines))
            if len(dataLines) > 0:
                texts[fileItem.fileName] = dataLines
    return texts


def correctDataLinesLength():
    originalMap = getAllDataLines()
    if not originalMap:
        print("Not map data is available")
    correctMap = {}
    for (k, v) in originalMap.items():
        counter = 0
        lenHeader = 0
        correctRows = []
        for row in v:
            if counter == 0: 
                '''add header'''
                lenHeader = len(row)
                correctRows.append(row)
            else:
                lenData = len(row)
                '''special row data'''
                if lenData > lenHeader:
                    print('before:' + str(row))
                    newRow = []
                    mergeStr = ''
                    for i, val in enumerate(row):
                        if (i + 1) >= lenHeader and (i + 1) < lenData:
                            mergeStr += val + ' '
                        elif (i + 1) == lenData:
                            mergeStr += val
                            newRow.append(mergeStr) 
                        else:
                            newRow.append(val)
                    print('after:' + str(newRow))
                elif lenData == lenHeader:
                    '''add ordinary row data'''
                    correctRows.append(row)
                else:
                    '''error row data'''
                    print('error row data:file_name=[' + k + '], row_data=' + row + ']')
            counter = counter + 1
        correctMap[k] = correctRows
    return correctMap   


def cleanSpecialWordDataLines():
    originalMap = correctDataLinesLength()
    if not originalMap:
        print("Not map data is available")
    correctMap = {}
    for (fileName, rowDatas) in originalMap.items():
        newRows = []
        for rowData in rowDatas:
            newRow = []
            for column in rowData:
                inFlag = False
                for filterKeyWord in filterDataKeyWords:
                    if filterKeyWord in column:
                        inFlag = True
                if inFlag:
                    newColumn = column
                    for filterKeyWord in filterDataKeyWords:
                        newColumn = newColumn.replace(filterKeyWord, '')
                    newRow.append(newColumn)
                else:
                    newRow.append(column)
            newRows.append(newRow)
        correctMap[fileName] = newRows       
    return correctMap


class CreditAccountAnalyzer(object):
    dcPath = os.path.join(BASE_DIR, 'Account' + os.path.sep + 'disbursement-channels.json')
    touPath = os.path.join(BASE_DIR, 'Account' + os.path.sep + 'type-of-use.json')
    descriptionColumnIndex = 5
    headerRowIndex = 0 
    disbursementNewColumn1 = "支付渠道名称"
    disbursementNewColumn2 = "支付渠道编码" 
    typeOfUseNewColumn1 = "使用类型名称"
    typeOfUseNewColumn2 = "使用类型编码" 
    
    def __init__(self, lines=[]):
        self.lines = lines
        self.dcData = self.listOrdinaryType(self.dcPath)
        self.touData = self.listOrdinaryType(self.touPath)
         
    def listOrdinaryType(self, path):
        with codecs.open(path, 'r', encoding) as json_file:
            data = json.load(json_file)
        defaultRow = None
        for i, row in enumerate(data):
            if i == 0:
                defaultRow = row
            if row['default']:
                defaultRow = row
                break
        return {"default":defaultRow, "rows":data}
    
    def getOrdinaryType(self, text, data):
        result = data['default']
        for key in data['rows']:
            if key["name"] in text:
                result = key
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
        return lines


class Account(object):

    def generateDataFile(self, path):
        data = cleanSpecialWordDataLines()
        analyzer = CreditAccountAnalyzer()
        result = []
        for key in data.keys():
            lines = data[key]
            result = result + analyzer.calculate(lines)
        generateFile(result, path)
        
        
if __name__ == '__main__':  
    a = Account()
    a.generateDataFile('/Users/summer/Desktop/account.txt')
