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


class AthleteList(list):

    def __init__(self, name, times=[]):
        list.__init__([])
        self.name = name
        self.extend(times)
    
    def top3(self):
        return sorted(set([sanitize(t) for t in self]))[0:3]

      
def getSourceData(n, p):
    with open(p) as d:
        data = d.readline()
    return AthleteList(n, data.strip().split(','))


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


def save(aps, items):
    try:
        if os.path.exists(aps):
            os.remove(aps)
        with open(aps, 'wb') as savedData:
            pickle._dump(items, savedData)
    except IOError as err:
        print('File error:' + str(err))

        
if __name__ == '__main__':      
    charles = getSourceData('charles', '..' + os.path.sep + 'Sorter' + os.path.sep + 'charles.txt')
    james = getSourceData('james', '..' + os.path.sep + 'Sorter' + os.path.sep + 'james.txt')
    ray = getSourceData('ray', '..' + os.path.sep + 'Sorter' + os.path.sep + 'ray.txt')
    summer = getSourceData('summer', '..' + os.path.sep + 'Sorter' + os.path.sep + 'summer.txt')
    r_all = {}
    r_all[charles.name] = sorted(charles.top3())
    r_all[james.name] = sorted(james.top3())
    r_all[ray.name] = sorted(ray.top3())
    r_all[summer.name] = sorted(summer.top3())
    report('..' + os.path.sep + 'Sorter' + os.path.sep + 'report.txt', r_all)
    save('..' + os.path.sep + 'Sorter' + os.path.sep + 'saved_report.txt', r_all)

