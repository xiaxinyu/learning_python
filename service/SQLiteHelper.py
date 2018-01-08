'''
Created on 2018.1.8

@author: summer.xia
@contact: summer_west2010@126.com
'''
import sqlite3
import os
from service.Sorter import getData
from service.Sorter import savedPath

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dbScriptPath = os.path.join(BASE_DIR, 'SQLiteHelper' + os.path.sep + 'create_table_script.sql')
dbPath = os.path.join(BASE_DIR, 'SQLiteHelper' + os.path.sep + 'athlete.sqlite')
insertScriptPath = os.path.join(BASE_DIR, 'SQLiteHelper' + os.path.sep + 'create_rowdata_script.sql')


def removeDatabaseFile(path):
    if os.path.exists(path):
        os.remove(path)

    
def getCreateTableScript(path):
    scripts = ''   
    try:
        f = open(path, 'r')
        lines = f.readlines()
        if len(lines) <= 0:
            return scripts
        for line in lines:
            scripts = scripts + line.strip()
    except Exception as e:
        print('Getting db scripts fail, message=' + str(e))
    finally:
        if 'f' in locals():
            f.close()
    return scripts


def initiateDatabase():
    removeDatabaseFile(dbPath)
    conn = sqlite3.connect(dbPath)
    print('Opened database successfully')
    scripts = getCreateTableScript(dbScriptPath)
    if scripts:
        conn.execute(scripts)
        conn.commit()
        print('Table created successfully')
    else:
        print('DB scripts is not available')
    conn.close()


def insertRowData(rows):
    if rows is None or len(rows) <= 0:
        print('No row datas are available')
        return
    scriptTemplate = getCreateTableScript(insertScriptPath)
    conn = sqlite3.connect(dbPath)
    if scriptTemplate:
        for row in rows:
            insertScript = scriptTemplate % (row['name'], row['time'])
            conn.execute(insertScript)
        conn.commit()
        print('Table created successfully')
    else:
        print('Insert script is not available')
    conn.close()


def batchInsertAthleteGrade():
    data = getData(savedPath)
    if not data:
        print('No athlete row datas are available')
        return
    names = data.keys()
    rows = []
    for key in names:
        times = data[key]        
        for time in times:
            row = {}
            row['name'] = key
            row['time'] = time
            rows.append(row)
    if len(rows) <= 0:
        print('Converting operation has error. please double check.')
        return
    insertRowData(rows)

def readAthleteGrades(name):
    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()
    sql = "select * from GRADE where NAME = '%s' " % name
    cur.execute(sql)
    items = []   
    for item in cur.fetchall():
        items.append(item)
    conn.close()
    return items
    
if __name__ == '__main__':
#     initiateDatabase()
#     batchInsertAthleteGrade()
    print(readAthleteGrades('summer'))  
