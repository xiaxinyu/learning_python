'''
Created on 2018.1.10

@author: summer.xia
@contact: summer_west2010@126.com
'''
from account.helper.FileHelper import generateFile
from account.analyzer.BusinessAnalyzer import BusinessAnalyzer
from account.cleaner.CreditAccountCleaner import CreditAccountCleaner
from account.cleaner.AlipayAccountCleaner import AlipayAccountCleaner
from account.helper.SQLiteHelper import SQLiteHelper
import os
from account.Combiner import combineCreditAndAlipay


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Account(object):

    def __init__(self, dataFilesPath=None, resultFilePath=None):
        self.dataFilesPath = dataFilesPath
        self.resultFilePath = resultFilePath
        
    def generateDataFile(self):
        creditCleaner = CreditAccountCleaner(self.dataFilesPath + os.path.sep + "credit")
        creditMatrix = creditCleaner.clean()
        generateFile(creditMatrix, self.resultFilePath + os.path.sep + "credit.txt")
        
        alipayCleaner = AlipayAccountCleaner(dataFilesPath + os.path.sep + "alipay")
        alipayMatrix = alipayCleaner.clean()   
        generateFile(alipayMatrix, self.resultFilePath + os.path.sep + "alipay.txt")
        
        conbine1 = combineCreditAndAlipay(creditMatrix, alipayMatrix)
        generateFile(conbine1, self.resultFilePath + os.path.sep + "conbine1.txt")
        
        analyzer = BusinessAnalyzer()
        result = analyzer.calculate(conbine1)
        
        generateFile(result, self.resultFilePath + os.path.sep + "result.txt")
        sqliteHelper = SQLiteHelper()
        sqliteHelper.initiateDatabase()
        sqliteHelper.batchInsert(result[1: len(result)])
        
if __name__ == '__main__':
#     dataFilesPath = '/Users/summer/Desktop/account'
    dataFilesPath = 'd:\\test'
    resultFilePath = 'd:\\result'
#     resultFilePath = '/Users/summer/Desktop/account.txt'
    a = Account(dataFilesPath, resultFilePath)
    a.generateDataFile()
