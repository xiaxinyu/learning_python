'''
Created on 2018.1.12

@author: summer.xia
@contact: summer_west2010@126.com
'''
from account.helper.StringHelper import isNotEmpty
from account.helper.StringHelper import parseDate
from account.helper.StringHelper import formatDateTime
from account.helper.FileHelper import getFiles
from account.helper.FileHelper import getAllLines


class CCBCreditCleaner(object):
    filterHeaderKeyWord = '交易明细'
    spliter = ' '
    filterDataKeyWords = ['CNY/']
    transactionDateIndex = 0
    recordDateIndex = 1
    currencyIndex = 4
    currencySpliter = '/'
    descriptionSpliter = ' '
    moneyIndex1 = 3
    moneyIndex2 = 5
   
    def __init__(self, dataFilesPath=None):
        self.dataFilesPath = dataFilesPath
    
    def getDataLines(self, lines):
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
            if self.filterHeaderKeyWord in line:
                startFlag = True
        return dataLines
    
    def generateMatrix(self, lines):
        if len(lines) < 0:
            return None
        matrix = []
        for line in lines:
            array = line.split(self.spliter)
            cleanArray1 = filter(isNotEmpty, array)
            cleanArray2 = []
            for (index, item) in enumerate(cleanArray1):
                if index == self.currencyIndex:
                    ''' get currency by splitting word '''
                    currencyItems = item.split(self.currencySpliter)
                    cleanArray2.append(currencyItems[0])
                    cleanArray2.append(currencyItems[1])
                else:
                    cleanArray2.append(item.strip())
            matrix.append(cleanArray2)
        return matrix
    
    def getAllDataLines(self):
        fileItems = getFiles(self.dataFilesPath)
        if not fileItems:
            print('No data files are available')
        texts = {}
        for fileItem in fileItems:
            lines = getAllLines(fileItem.absolutePath)
            if lines is None or len(lines) <= 0:
                continue                
            dataLines = self.generateMatrix(self.getDataLines(lines))
            if len(dataLines) <= 0:                continue
            
            texts[fileItem.fileName] = dataLines
        return texts
    
    def correctOverLengthRow(self, oldRow, lenHeader, lenData):
        newRow = []
        mergeStr = ''
        for i, val in enumerate(oldRow):
            position = (i + 1)
            if  position >= lenHeader and position < lenData:
                mergeStr += val + self.descriptionSpliter
            elif position == lenData:
                mergeStr += val
                newRow.append(mergeStr)
            else:
                newRow.append(val)
        return newRow
    
    def filterSpecialWord(self, column):
        newColumn = column
        inFlag = False
        for filterKeyWord in self.filterDataKeyWords:
            if filterKeyWord in column:
                inFlag = True
        if inFlag:            
            for filterKeyWord in self.filterDataKeyWords:
                newColumn = newColumn.replace(filterKeyWord, '')
        return newColumn
    
    def filterRowData(self, rowData):
        newRows = []
        for index, column in enumerate(rowData):
            if index == self.transactionDateIndex or index == self.recordDateIndex:
                newRows.append(formatDateTime(parseDate(column)))
            elif index == self.moneyIndex1 or index == self.moneyIndex2:
                newRows.append(float(self.filterSpecialWord(column)))
            else:
                newRows.append(self.filterSpecialWord(column))
        return newRows
    
    def correct(self):
        originalMap = self.getAllDataLines()
        if not originalMap:
            print("Not map data is available")
        correctMap = {}
        for (k, v) in originalMap.items():
            correctRows = []
            for (index, row) in enumerate(v):
                correctRow = row
                if index == 0:                 
                    lenHeader = len(correctRow)
                    correctRows.append(correctRow)
                    continue                
                else:
                    lenData = len(row)                    
                    if lenData > lenHeader:
                        ''' over long row data '''
                        print('before:' + str(row))
                        correctRow = self.correctOverLengthRow(row, lenHeader, lenData)
                        print('after:' + str(correctRow))                       
                    elif lenData < lenHeader:
                        '''error row data'''
                        print('error row data:file_name=[' + k + '], row_data=' + str(row) + ']')
                correctRows.append(self.filterRowData(correctRow))
            correctMap[k] = correctRows
        return correctMap
    
    def clean(self):
        originalMap = self.correct()
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
