'''
Created on 2018.1.26

@author: summer.xia
@contact: summer_west2010@126.com
'''
import numpy as np


def addPointedColumn(matrix, coloumnText):
    a = np.array(matrix)
    b = np.full(len(matrix), coloumnText)
    return np.c_[b, a].tolist()


def mergeMatrixsAandB(matrixA, matrixB):
    a = np.array(matrixA)
    b = np.array(matrixB)
    return np.concatenate((a,b),axis=0).tolist()
