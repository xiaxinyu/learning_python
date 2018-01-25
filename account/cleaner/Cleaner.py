'''
Created on 2018.1.25

@author: summer.xia
@contact: summer_west2010@126.com
'''
class Cleaner(object):    
    def getCleanHeader(self, array):
        cleanHeader = []
        for header in array:
            header = header.strip()
            if header:
                cleanHeader.append(header)
        return cleanHeader
    
    def cleanHeader(self, originalMap):
        if not originalMap:
            print("Not map data is available")
        result = []
        counter = 0
        for key in originalMap.keys():
            finalRowDatas = originalMap[key]
            if counter != 0 and len(finalRowDatas) > 1:
                finalRowDatas = finalRowDatas[1: len(finalRowDatas)]
            result = result + finalRowDatas
            counter = counter + 1      
        return result
    
