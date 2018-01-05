'''
Created on 2018年1月5日

@author: summer.xia
@contact: summer_west2010@126.com
'''
import os
import logging
import codecs

logging.basicConfig(filename='d:\\FileJoiner.log',level=logging.DEBUG,)

class FileItem(object):

    def __init__(self, fn, ap):
        self.fn = fn
        self.ap = ap

    
class TextItem(object):

    def __init__(self, fn, lines):
        self.fn = fn
        self.lines = lines

        
class Line(object):

    def __init__(self, h, text):
        self.h = h
        self.text = text

        
def getFiles(directoryPath):
    r = []
    fs = os.listdir(directoryPath)
    '''check whether files is null'''
    if fs is None or len(fs) <= 0:
        return r
    '''get absolute path by loop'''
    for f in fs:
        ap = os.path.join(directoryPath, f)
        r.append(FileItem(f, ap))
    return r

    
def readFile(fi):
    try:
        '''check whether file exist '''
        print(fi.ap)
        if not os.path.exists(fi.ap):
            return None
        file = codecs.open(fi.ap, 'r', 'utf-8')
        '''check whether texts is null'''
        if file is None:
            return None
        rows = []
        '''get each line by loop'''
        for each_line in file:
            rows.append(each_line.strip())
        return TextItem(fi.fn, rows)
    except Exception as e:
        logging.exception('Reading file has error. [' +  str(e) +']')
    finally:
        if 'file' in locals():
            file.close() 
    return None

    
def joinFiles(path, txtObjs, showFn=True):
    try:
        if txtObjs is None or len(txtObjs) <= 0:
            return 
        if os.path.exists(path):
            os.remove(path)
        lines = []
        for txtObj in txtObjs:
            for row in txtObj.lines:
                lines.append(Line(txtObj.fn, row)) 
        
        file = open(path, 'w')   
        for l in lines:
            if showFn:
                file.write(l.h + ':' + l.text+'\r\n')
            else:
                file.write(l.text+'\r\n')
    except Exception as e:
        logging.exception('Reading file has error. [' +  str(e) +']')
    finally :
        if 'file' in locals():
            file.close()     

        
def merge(sp, dp, showFn):
    items = getFiles(sp)
    if items is None or len(items) <= 0:
        return    
    texts = []
    for item in items:
        text = readFile(item)
        if text is not None:
            texts.append(text)                
    joinFiles(dp, texts, showFn)            

            
if __name__ == '__main__':  
    merge('D:\\test', 'D:\\TEST.txt', True)
    
