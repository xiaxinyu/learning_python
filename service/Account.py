'''
Created on 2018.1.10

@author: summer.xia
@contact: summer_west2010@126.com
'''
from service.FileHelper import getFiles
from service.FileHelper import getAllLines

directoryPath = '/Users/summer/Desktop/account'
encoding = 'utf-8'
filterKeyWord = '交易明细'


def getDataLines(lines):
    if len(lines) < 0:
        return None
    startFlag = False
    dataLines = []
    for line in lines:
        if startFlag:
            dataLines.append(line)
        if filterKeyWord in line:
            startFlag = True
    return dataLines


def getAllDataLines():
    fileItems = getFiles(directoryPath)
    if not fileItems:
        print('No data files are available')
    texts = {}
    for fileItem in fileItems:
        lines = getAllLines(fileItem.absolutePath, encoding)
        if lines is not None and len(lines) > 0:
            dataLines = getDataLines(lines)
            if len(dataLines) > 0:
                texts[fileItem.fileName] = dataLines
    print(texts)


if __name__ == '__main__':  
    getAllDataLines()

