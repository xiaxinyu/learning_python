'''
Created on 2018.1.12

@author: summer.xia
@contact: summer_west2010@126.com
'''
from account.StringHelper import isNotEmpty
from account.FileHelper import getFiles
from account.FileHelper import getAllLines


class CreditAccountCleaner(object):
    encoding = 'utf-8'
    filterHeaderKeyWord = '交易明细'
    spliter = ' '
    filterDataKeyWords = ['CNY/', '人民币/']
   
    def __init__(self, dataFilesPath=None):
        self.dataFilesPath = dataFilesPath
    
    def getAllDataLines(self):
        fileItems = getFiles(self.dataFilesPath)
        if not fileItems:
            print('No data files are available')
        texts = {}
        for fileItem in fileItems:
            lines = getAllLines(fileItem.absolutePath, self.encoding)
            if lines is not None and len(lines) > 0:
                dataLines = self.generateAccountMatrix(self.getDataLines(lines))
                if len(dataLines) > 0:
                    texts[fileItem.fileName] = dataLines
        return texts
    
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

    def  generateAccountMatrix(self, lines):
        if len(lines) < 0:
            return None
        matrix = []
        for line in lines:
            array = line.split(self.spliter)
            cleanArray1 = filter(isNotEmpty, array)
            cleanArray2 = []
            for item in cleanArray1:
                cleanArray2.append(item.strip())
            matrix.append(cleanArray2)
        return matrix
    

    def correctDataLinesLength(self):
        originalMap = self.getAllDataLines()
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

    def cleanSpecialWordDataLines(self):
        originalMap = self.correctDataLinesLength()
        if not originalMap:
            print("Not map data is available")
        correctMap = {}
        for (fileName, rowDatas) in originalMap.items():
            newRows = []
            for rowData in rowDatas:
                newRow = []
                for column in rowData:
                    inFlag = False
                    for filterKeyWord in self.filterDataKeyWords:
                        if filterKeyWord in column:
                            inFlag = True
                    if inFlag:
                        newColumn = column
                        for filterKeyWord in self.filterDataKeyWords:
                            newColumn = newColumn.replace(filterKeyWord, '')
                        newRow.append(newColumn)
                    else:
                        newRow.append(column)
                newRows.append(newRow)
            correctMap[fileName] = newRows       
        return correctMap
