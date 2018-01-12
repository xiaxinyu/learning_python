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
        data = cleaner.cleanSpecialWordDataLines()
        analyzer = CreditAccountAnalyzer()
        result = []
        for key in data.keys():
            lines = data[key]
            result = result + analyzer.calculate(lines)
        generateFile(result, self.resultFilePath)
        
        
if __name__ == '__main__':
    # directoryPath = '/Users/summer/Desktop/account'
    dataFilesPath = 'd:\\test'
    resultFilePath = 'd://account.txt'
    a = Account(dataFilesPath, resultFilePath)
    a.generateDataFile()
