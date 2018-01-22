'''
Created on 2018.1.10

@author: summer.xia
@contact: summer_west2010@126.com
'''
from account.FileHelper import generateFile
from account.CreditAccountAnalyzer import CreditAccountAnalyzer
from account.CreditAccountCleaner import CreditAccountCleaner
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Account(object):

    def __init__(self, dataFilesPath=None, resultFilePath=None):
        self.dataFilesPath = dataFilesPath
        self.resultFilePath = resultFilePath
        
    def generateDataFile(self):
        cleaner = CreditAccountCleaner(self.dataFilesPath)
        originalData = cleaner.clean()
        analyzer = CreditAccountAnalyzer()
        cleanMap = {}        
        for key in originalData.keys():
            cleanMap[key] = analyzer.calculate(originalData[key])
        result = cleaner.cleanNeedlessHeader(cleanMap) 
        generateFile(result, self.resultFilePath)
        
        
if __name__ == '__main__':
#     dataFilesPath = '/Users/summer/Desktop/account'
    dataFilesPath = 'd:\\test'
    resultFilePath = 'd://account.txt'
#     resultFilePath = '/Users/summer/Desktop/account.txt'
    a = Account(dataFilesPath, resultFilePath)
    a.generateDataFile()
