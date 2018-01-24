'''
Created on 2018.1.10

@author: summer.xia
@contact: summer_west2010@126.com
'''
from account.helper.FileHelper import generateFile
from account.analyzer.BusinessAnalyzer import BusinessAnalyzer
from account.cleaner.CreditAccountCleaner import CreditAccountCleaner
from account.helper.SQLiteHelper import SQLiteHelper
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Account(object):

    def __init__(self, dataFilesPath=None, resultFilePath=None):
        self.dataFilesPath = dataFilesPath
        self.resultFilePath = resultFilePath
        
    def generateDataFile(self):
        cleaner = CreditAccountCleaner(self.dataFilesPath)
        originalData = cleaner.clean()
        analyzer = BusinessAnalyzer()
        cleanMap = {}        
        for key in originalData.keys():
            cleanMap[key] = analyzer.calculate(originalData[key])
        result = cleaner.cleanNeedlessHeader(cleanMap)
        generateFile(result, self.resultFilePath)
        '''save data to SQLite'''
        sqliteHelper = SQLiteHelper()
        sqliteHelper.initiateDatabase()
        sqliteHelper.batchInsert(result[1: len(result)])
        
        
if __name__ == '__main__':
#     dataFilesPath = '/Users/summer/Desktop/account'
    dataFilesPath = 'd:\\test'
    resultFilePath = 'd://account.txt'
#     resultFilePath = '/Users/summer/Desktop/account.txt'
    a = Account(dataFilesPath, resultFilePath)
    a.generateDataFile()
