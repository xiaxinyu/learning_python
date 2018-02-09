'''
Created on 2018.2.9

@author: summer.xia
@contact: summer_west2010@126.com
'''
import codecs
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.path.sep + 'static' + os.path.sep
ctPath = os.path.join(BASE_DIR, 'consumption-type.json')
ctResultPath = os.path.join(BASE_DIR, 'consume-datasource.js')

def generateConsumptionType(target, destination, encoding='utf-8'):
    with codecs.open(target, 'r', encoding) as t_file:
        data = json.load(t_file)
    
    for node in data:
        for leaf in node['children']:
            if 'keyWords' in leaf:
                del leaf['keyWords']
            if 'default' in leaf:
                del leaf['default']
                
    d_file = codecs.open(destination, 'w', encoding)
    d_file.write(json.dumps(data, ensure_ascii=False))
    d_file.flush()
    d_file.close()

if __name__ == '__main__':
    generateConsumptionType(ctPath, ctResultPath)
    