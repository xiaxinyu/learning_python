'''
Created on 2018.1.25

@author: summer.xia
@contact: summer_west2010@126.com
'''
from account.helper.FileHelper import generateFile
from account.helper.FileHelper import getFiles
from account.helper.StringHelper import isNotEmpty
from account.helper.FileHelper import getAllLines
from account.cleaner.Cleaner import Cleaner
import numpy as np


class CCBCreditCleaner(Cleaner):
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
    
    def clean(self):
        rowDatas = super().cleanHeader(self.getAllDataLines())
        if rowDatas is None or len(rowDatas) <= 0:
            return
        t = np.array(rowDatas)
        account = np.full(len(rowDatas), self.accountNumber)
        result = np.c_[t,account]
        a = np.array_str(result[:,0])
        b = np.array_str(result[:,2])
        summer = np.append(a,b)
        print(a)
        print(b)
        print(summer)
        
                
        
    
cleaner = CCBCreditCleaner("d:\\test\\deposits")
result = cleaner.clean()
#generateFile(result, "d:\\result\\deposits.txt")


