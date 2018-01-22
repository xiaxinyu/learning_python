'''
Created on 2018.1.17

@author: summer.xia
@contact: summer_west2010@126.com
'''
import os
import sqlite3
from account.FileHelper import getText 


class SQLiteHelper(object):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + 'account' + os.path.sep + 'static' + os.path.sep
    createPath = os.path.join(BASE_DIR, 'create_table_sqlite.sql')
    insertPath = os.path.join(BASE_DIR, 'create_rowdata_sqlite.sql')
    databasePath = os.path.join(BASE_DIR, 'account.sqlite')
    
    def __init__(self, dataSet):
        print(dataSet)

    def removeDatabase(self, path):
        if os.path.exists(path):
            os.remove(path)
    
    def initiateDatabase(self):
        self.removeDatabaseFile(self.databasePath)
        conn = sqlite3.connect(self.databasePath)
        scripts = getText(self.createPath)
        if scripts:
            conn.execute(scripts)
            conn.commit()
            print('Table created successfully')
        else:
            print('DB scripts is not available')
        conn.close()
    
    def insertRow(self, conn, scripts, columns):
        if columns is None or len(columns) <= 0:
            print('Columns are not available')
            return
       
        insertScript = scripts % (columns['name'], columns['time'])
        conn.execute(insertScript)
        print('Table created successfully')
    
    def batchInsertAthleteGrade(self, dataRows):
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
        else:
            print('Insert script is not available')
