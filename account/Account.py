'''
Created on 2018.1.10

@author: summer.xia
@contact: summer_west2010@126.com
'''
from account.helper.FileHelper import generateFile
from account.analyzer.BusinessAnalyzer import BusinessAnalyzer
from account.cleaner.CCBCreditCleaner import CCBCreditCleaner
from account.cleaner.CCBDepositsCleaner import CCBDepositsCleaner
from account.cleaner.AlipayAccountCleaner import AlipayAccountCleaner
from account.db.SQLiteHelper import SQLiteHelper
import os
from account.Combiner import combineCCBAndAlipay
from account.helper.MatrixHelper import addPointedColumn
from account.helper.MatrixHelper import mergeMatrixsAandB
from account.db.OracleHelper import OrderHelper


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Account(object):

    def __init__(self, dataFilesPath=None, resultFilePath=None):
        self.dataFilesPath = dataFilesPath
        self.resultFilePath = resultFilePath
        
    def generateDataFile(self):
        ccbCreditCleaner = CCBCreditCleaner(self.dataFilesPath + os.path.sep + "credit")
        ccbCreditMatrix = ccbCreditCleaner.clean()
        generateFile(ccbCreditMatrix, self.resultFilePath + os.path.sep + "credit.txt")
        
        ccbDepositesCleaner = CCBDepositsCleaner(self.dataFilesPath + os.path.sep + "deposits")
        ccbDepositesMatrix = ccbDepositesCleaner.clean()
        generateFile(ccbDepositesMatrix, self.resultFilePath + os.path.sep + "deposits.txt")
        
        alipayCleaner = AlipayAccountCleaner(dataFilesPath + os.path.sep + "alipay")
        alipayMatrix = alipayCleaner.clean()   
        generateFile(alipayMatrix, self.resultFilePath + os.path.sep + "alipay.txt")
        
        conbine1 = combineCCBAndAlipay(ccbCreditMatrix, alipayMatrix)
        generateFile(conbine1, self.resultFilePath + os.path.sep + "conbine1.txt")
        
        conbine2 = combineCCBAndAlipay(ccbDepositesMatrix, alipayMatrix)
        generateFile(conbine2, self.resultFilePath + os.path.sep + "conbine2.txt")
        
        analyzer = BusinessAnalyzer()
        ccbCredit = addPointedColumn(analyzer.calculate(conbine1), 'credit')
        ccbDeposites = addPointedColumn(analyzer.calculate(conbine2), 'deposites')
        
        result = mergeMatrixsAandB(ccbCredit, ccbDeposites[1: len(ccbDeposites)])
        generateFile(result, self.resultFilePath + os.path.sep + "result.txt")
        
        sqliteHelper = SQLiteHelper()
        sqliteHelper.initiateDatabase()
        sqliteHelper.batchInsert(result[1: len(result)])
        
        oracleHelper = OrderHelper()
        oracleHelper.batchInsert(result[1: len(result)])
        
if __name__ == '__main__':
#     dataFilesPath = '/Users/summer/Desktop/account'
    dataFilesPath = 'd:\\test'
    resultFilePath = 'd:\\result'
#     resultFilePath = '/Users/summer/Desktop/account.txt'
    a = Account(dataFilesPath, resultFilePath)
    a.generateDataFile()
