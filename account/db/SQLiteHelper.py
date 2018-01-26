'''
Created on 2018.1.17

@author: summer.xia
@contact: summer_west2010@126.com
'''
import os
import sqlite3
from account.helper.FileHelper import getText 


class SQLiteHelper(object):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.path.sep + 'static' + os.path.sep
    createPath = os.path.join(BASE_DIR, 'create_table_sqlite.sql')
    insertPath = os.path.join(BASE_DIR, 'insert_table_sqlite.sql')
    databasePath = os.path.join(BASE_DIR, 'account.sqlite')
    
    def removeDatabase(self, path):
        if os.path.exists(path):
            os.remove(path)
    
    def initiateDatabase(self):
        self.removeDatabase(self.databasePath)
        conn = sqlite3.connect(self.databasePath)
        scripts = getText(self.createPath)
        if scripts:
            conn.execute(scripts)
            conn.commit()
            print('Table create successfully')
        else:
            print('DB scripts is not available')
        conn.close()
    
    def insertRow(self, conn, scripts, columns):
        if columns is None or len(columns) <= 0:
            print('Columns are not available')
            return
        insertScript = scripts % (columns[0], columns[1], columns[2], columns[3], columns[4], columns[5], columns[6], columns[7], columns[8], columns[9], columns[10], columns[11], columns[12], columns[13], columns[14], columns[14])
        conn.execute(insertScript)
    
    def batchInsert(self, dataRows):
        if not dataRows or len(dataRows) <= 0:
            print('Row data are not available')
            return
        scripts = getText(self.insertPath)
        if scripts:
            conn = sqlite3.connect(self.databasePath)
            for dataRow in dataRows:
                self.insertRow(conn, scripts, dataRow)
            conn.commit() 
            conn.close()
            print('DataRows create successfully')
        else:
            print('Insert script is not available')
