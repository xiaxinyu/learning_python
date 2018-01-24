'''
Created on 2018.1.23

@author: summer.xia
@contact: summer_west2010@126.com
'''
from account.helper.FileHelper import getFiles
from account.helper.FileHelper import getAllLines
from account.helper.FileHelper import generateFile


class AlipayAccountCleaner(object):
    encoding = 'gbk'
    filterHeadKeyWord = '交易记录明细列表'
    filterTailKeyWord = '-----------------------------------------'
    spliter = ','
    moneyIndex = 9
    
    def __init__(self, dataFilesPath=None):
        self.dataFilesPath = dataFilesPath
        
    def getDataLines(self, lines):
        if len(lines) < 0:
            return None
        headFlag = False
        dataLines = []
        for line in lines:
            if self.filterHeadKeyWord in line:
                headFlag = True
                continue
            if self.filterTailKeyWord in line:
                break
            if headFlag:                
                dataLines.append(line)
        return dataLines
    
    def getCleanHeader(self, array):
        cleanHeader = []
        for header in array:
            header = header.strip()
            if header:
                cleanHeader.append(header)
        return cleanHeader
                        
    def generateMatrix(self, lines):
        if len(lines) < 0:
            return None
        matrix = []
        headerLength = 0 
        for (index, line) in enumerate(lines):
            array = line.split(self.spliter)
            if index == 0:
                cleanHeader = self.getCleanHeader(array)
                headerLength = len(cleanHeader)
                matrix.append(cleanHeader)
                continue
            if len(array) >= headerLength:
                cleanArray1 = array[0: headerLength]
                cleanArray2 = []
                for (index, item) in enumerate(cleanArray1):
                    if index == self.moneyIndex:
                        cleanArray2.append(float(item.strip()))
                    else:
                        cleanArray2.append(item.strip())                        
                matrix.append(cleanArray2)
            else:
                print('error apliay row data, length:[ ' + str(len(array)) + ' ]: ' + str(line))
        return matrix
        
    def getAllDataLines(self):
        fileItems = getFiles(self.dataFilesPath)
        if not fileItems:
            print('Alipay data files are not available')
        texts = {}
        for fileItem in fileItems:
            lines = getAllLines(fileItem.absolutePath, self.encoding)
            if lines is None or len(lines) <= 0:
                continue                
            dataLines = self.generateMatrix(self.getDataLines(lines))
            if len(dataLines) <= 0:                
                continue
            texts[fileItem.fileName] = dataLines
        return texts
    
    def clean(self):
        originalMap = self.getAllDataLines()
        if not originalMap:
            print("Not map data is available")
        result = []
        counter = 0
        for key in originalMap.keys():
            finalRowDatas = originalMap[key]
            if counter != 0 and len(finalRowDatas) > 1:
                finalRowDatas = finalRowDatas[1: len(finalRowDatas)]
            result = result + finalRowDatas
            counter = counter + 1      
        return result
    
    def checkLength(self, dataRows):
        error = []
        if dataRows is not None and len(dataRows) > 0:
            headerLength = 0;
            for (index, dataRow) in enumerate(dataRows):
                if index == 0:
                    headerLength = len(dataRow)
                    error.append('header length is ' + str(headerLength))
                else:
                    if headerLength != len(dataRow):
                        error.append('error apliay row data position: [' + str(index + 1) + '], length:[ ' + str(len(dataRow)) + ' ]: ' + str(dataRow))
                        
        return error
            

if __name__ == '__main__':
    dataFilesPath = 'd:\\test\\alipay\\'
    resultFilePath = 'd://alipay.txt'
    a = AlipayAccountCleaner(dataFilesPath)
    result = a.getAllDataLines()    
    dataRows = result['alipay_record_20180123_1054_1.csv'];
    generateFile(dataRows, resultFilePath)
    error = a.checkLength(dataRows)
    generateFile(error, 'd://alipay-error.txt')
