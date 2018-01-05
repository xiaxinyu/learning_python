'''
Created on 2018.1.5

@author: summer.xia
@contact: summer_west2010@126.com
'''
import os
import pickle

def sanitize(time):
    if '-' in time:
        splitter = '-'
    elif ':' in time:
        splitter = ':'
    else:
        return time
    (mins, secs) = time.split(splitter)
    return mins + '.' + secs

    
def getSourceData(p):
    with open(p) as d:
        data = d.readline()
    return data.strip().split(',')


def eliminateRepetition(items):
    result = []
    for item in items:
        c_item = sanitize(item);
        if c_item not in result:
            result.append(c_item)
    return result


def merge(aList, bList):
    result = []
    result.append(aList)
    result.append(bList)
    return result


def report(aps, items):
    try:
        if os.path.exists(aps):
            os.remove(aps)
        with open(aps, 'w') as mysavedata:
            pickle._dump(items, mysavedata)
    except IOError as err:
        print('File error:' + str(err))
    except pickle.PickleError as perr:
        print('Pickling error:' + str(perr))
        
            
charles = getSourceData('Sorter\\charles.txt')
james = getSourceData('Sorter\\james.txt')
ray = getSourceData('Sorter\\ray.txt')
summer = getSourceData('Sorter\\summer.txt')

c_charles = eliminateRepetition(charles)
c_james = eliminateRepetition(james)
c_ray = eliminateRepetition(ray)
c_summer = eliminateRepetition(summer)

r_charles = sorted(c_charles[0:3])
r_james = sorted(c_james[0:3])
r_ray = sorted(c_ray[0:3])
r_summer = sorted(c_summer[0:3])

r_all = merge(merge(merge(r_charles, r_james), r_ray), r_summer)

report('Sorter\\report.txt', r_all)

