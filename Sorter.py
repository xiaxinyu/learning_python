'''
Created on 2018.1.5

@author: summer.xia
@contact: summer_west2010@126.com
'''
import os


def sanitize(time):
    if '-' in time:
        splitter = '-'
    elif ':' in time:
        splitter = ':'
    else:
        return time
    (mins, secs) = time.split(splitter)
    return mins + '.' + secs


class AtheleteList(list):

    def __init__(self, name, times=[]):
        list.__init__([])
        self.name = name
        self.extend(times)
    
    def top3(self):
        return sorted(set([sanitize(t) for t in self]))[0:3]

      
def getSourceData(n, p):
    with open(p) as d:
        data = d.readline()
    return AtheleteList(n, data.strip().split(','))


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
    charles = getSourceData('charles', 'Sorter/charles.txt')
    james = getSourceData('james', 'Sorter/james.txt')
    ray = getSourceData('ray', 'Sorter/ray.txt')
    summer = getSourceData('summer', 'Sorter/summer.txt')
    r_all = {}
    r_all[charles.name] = sorted(charles.top3())
    r_all[james.name] = sorted(james.top3())
    r_all[ray.name] = sorted(ray.top3())
    r_all[summer.name] = sorted(summer.top3())
    report('Sorter/report.txt', r_all)

