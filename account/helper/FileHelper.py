'''
Created on 2018.1.10

@author: summer.xia
@contact: summer_west2010@126.com
'''
import os
import codecs


class FileItem(object):

    def __init__(self, fileName, absolutePath):
        self.fileName = fileName
        self.absolutePath = absolutePath


def getText(absolutePath, encoding='utf-8'):
    try:
        if not os.path.exists(absolutePath):
            return None
        f = codecs.open(absolutePath, 'r', encoding)
        lines = f.readlines()
        if len(lines) <= 0:
            return None
        texts = ''
        for line in lines:
            texts = texts + line.strip()
        return texts
    except Exception as e:
        print('Reading text fail, message=' + str(e))
    finally:
        if 'f' in locals():
            f.close()
    return None

    
def getFiles(directoryPath):
    files = os.listdir(directoryPath)
    if files is None or len(files) <= 0:
        return None
    items = []
    for file in files:
        absolutePath = os.path.join(directoryPath, file)
        items.append(FileItem(file, absolutePath))
    return items


def getAllLines(absolutePath, encoding='utf-8'):
    if not os.path.exists(absolutePath):
        return None
    lines = []
    try:
        file = codecs.open(absolutePath, 'r', encoding)
        texts = file.readlines()
        if len(texts) <= 0:
            return None
        for text in texts:
            line = text.strip().replace('\r', '').replace('\n', '')
            if len(line) > 0:
                lines.append(line)
    except Exception as e:
        print('Getting all texts has error, message = [' + str(e) + ']')
    finally:
        if 'file' in locals():
            file.close()
    return lines


def generateFile(lines, path, encoding='utf-8'):
    try:
        if lines is None or len(lines) <= 0:
            print('No available data can be exported to file')
            return 
        if os.path.exists(path):
            os.remove(path)
        
        file = codecs.open(path, 'w', encoding)   
        for line in lines:
            file.write(str(line) + '\n')
    except Exception as e:
            print('Generating file has error. message [' + str(e) + ']')
    finally :
        if 'file' in locals():
            file.close()     
