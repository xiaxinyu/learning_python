'''
Created on 2018.1.5

@author: summer.xia
@contact: summer_west2010@126.com
'''
import os
from test.test_decimal import file


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


def report(aps, items):
    try:
        if os.path.exists(aps):
            os.remove(aps)
        file = open(aps, 'w')
        for key in items:
            file.write(str(key) + ':' + str(items[key]) + '\n')    
    except IOError as err:
        print('File error:' + str(err))
    finally:
        if 'file' in locals():
            file.close()

        
if __name__ == '__main__':      
    charles = getSourceData('Sorter/charles.txt')
    james = getSourceData('Sorter/james.txt')
    ray = getSourceData('Sorter/ray.txt')
    summer = getSourceData('Sorter/summer.txt')    
    c_charles = eliminateRepetition(charles)
    c_james = eliminateRepetition(james)
    c_ray = eliminateRepetition(ray)
    c_summer = eliminateRepetition(summer)    
    r_all = {}
    r_all['c_charles'] = sorted(c_charles[0:3])
    r_all['c_james'] = sorted(c_james[0:3])
    r_all['c_ray'] = sorted(c_ray[0:3])
    r_all['c_summer'] = sorted(c_summer[0:3])
    report('Sorter/report.txt', r_all)

