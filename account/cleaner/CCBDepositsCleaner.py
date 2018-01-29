'''
Created on 2018.1.25

@author: summer.xia
@contact: summer_west2010@126.com
'''
from account.helper.FileHelper import generateFile
from account.helper.FileHelper import getFiles
from account.helper.FileHelper import getAllLines
from account.cleaner.Cleaner import Cleaner
from account.helper.StringHelper import parseDateTime
from account.helper.StringHelper import formatDateTime
import numpy as np

class CCBDepositsCleaner(Cleaner):
    filterHeaderKeyWord = '记账日'
    filterAccountKeyWord = '账　　号'
    accountNumber = ''
    spliter = ','
    
    def __init__(self, dataFilesPath=None):
        self.dataFilesPath = dataFilesPath
    
    def getDataLines(self, lines):
        if len(lines) < 0:
            return None
        startFlag = False
        dataLines = []
        for line in lines:
            if self.filterHeaderKeyWord in line:
                startFlag = True
            elif self.filterAccountKeyWord in line:
                self.accountNumber = line.split('：')[1].strip()        
            if startFlag:
                dataLines.append(line)
        return dataLines
    
    def generateMatrix(self, lines):
        if len(lines) < 0:
            return None
        matrix = []
        headerLength = 0
        for (index, line) in enumerate(lines):
            array = line.split(self.spliter)
            if index == 0:
                header = super().getCleanHeader(array)
                headerLength = len(header)
                matrix.append(header)
                continue
            
            if array is not None and len(array) >= headerLength:
                cleanArray1 = array[0: headerLength]
                cleanArray2 = []
                for column in cleanArray1:
                    cleanArray2.append(column.strip())
                matrix.append(cleanArray2)
            else:
                print('error CCB deposits row data, length:[ ' + str(len(array)) + ' ]: ' + str(line))
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
    
    def formatDate(self, dates, times):
        for (index, date) in enumerate(dates):
            if index == 0:
                continue
            dates[index] = formatDateTime(parseDateTime(date + times[index]))
        return dates
    
    def fomatMoney(self, incomes, outcomes):
        for (index, income) in enumerate(incomes):
            if index == 0:
                continue
            if len(income) > 0:
                incomes[index] = float(income)
            else:
                outcome = outcomes[index]
                if len(outcome) > 0:
                    incomes[index] = float(outcome)
                else:
                    incomes[index] = 0
        return incomes
    
    def formatBlance(self, blances):
        for (index, blance) in enumerate(blances):
            if index == 0:
                continue
            if len(blance) > 0:
                blances[index] = float(blance)
            else:
                blances[index] = 0
        return blances
    
    def formatDigest(self, locations, oppositeAccounts, oppisiteNames, digests):
        result = []
        for (index, digest) in enumerate(digests): 
            if index == 0:
                result.append(digest)
                continue
            allStr = ''.join([str(locations[index]),"@@",str(oppositeAccounts[index]),"@@",str(oppisiteNames[index]),"@@", str(digest)])
            result.append(allStr)
        return result
            
    def clean(self):
        rowDatas = super().cleanHeader(self.getAllDataLines())
        if rowDatas is None or len(rowDatas) <= 0:
            return
        array = np.array(rowDatas)       
        c_a = self.formatDate(array[:, 0], array[:, 2])
        c_b = self.formatDate(array[:, 1], array[:, 2])
        c_c = np.full(len(rowDatas), self.accountNumber)
        c_d = self.fomatMoney(array[:, 4], array[:, 5]) 
        c_e = array[:, 9]
        c_f = self.formatBlance(array[:, 6])
        c_g = self.formatDigest(array[:, 3], array[:, 7], array[:, 8], array[:, 10])
        result = []
        for index in range(0,len(rowDatas)):
            rowData = []
            rowData.append(c_a[index])
            rowData.append(c_b[index])
            rowData.append(c_c[index])
            rowData.append(c_d[index])
            rowData.append(c_e[index])
            rowData.append(c_f[index])
            rowData.append(c_g[index])
            result.append(rowData)
        return result

