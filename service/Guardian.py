'''
Created on 2018.1.5

@author: summer.xia
@contact: summer_west2010@126.com
'''
import pickle

try:
    with open('Guardian\\readme.txt', 'wb') as mysavedata:
        pickle._dump([1, 2, 'three'], mysavedata)
    
    with open('Guardian\\readme.txt', 'rb') as myrestoredata:
        a_list = pickle.load(myrestoredata)
    print(a_list)
except IOError as err:
    print('File error:' + str(err))
except pickle.PickleError as perr:
    print('Pickling error:' + str(perr))
# if __name__ == '__main__':
#     pass
