'''
Created on 2018.1.17

@author: summer.xia
@contact: summer_west2010@126.com
'''
import cx_Oracle as oracle
from account.helper.StringHelper import getUUID


class OrderHelper(object):    
        
    def batchInsert(self, dataRows):
        conn = oracle.connect('scott/summer@127.0.0.1:1521/ORCL')  
        cursor = conn.cursor()
        
        recordID = str(getUUID())
        for dataRow in dataRows:
            uuid = str(getUUID())
            params = {"v_id": uuid, "v_card_id": dataRow[3], "v_transaction_date":dataRow[1], "v_bookkeeping_date":dataRow[2], "v_transaction_desc" : dataRow[7], "v_balance_currency" : dataRow[5], "v_balance_money": dataRow[4], "v_card_type_id":1, "v_card_type_name":"中国建设银行购物卡", "v_consumption_type": dataRow[11], "v_consume_id": dataRow[13], "v_consume_name" : dataRow[12], "v_demoarea": dataRow[14], "v_recordid":recordID, "v_payment_type_id":dataRow[9]}
            cursor.execute("insert into credit (id, card_id, transaction_date, bookkeeping_date, transaction_desc, balance_currency, balance_money, card_type_id, card_type_name, consumption_type, consume_id, consume_name, demoarea, recordid, payment_type_id) values(:v_id, :v_card_id, to_date(:v_transaction_date, 'yyyy-MM-dd HH24:mi:ss'), to_date(:v_bookkeeping_date, 'yyyy-MM-dd HH24:mi:ss'), :v_transaction_desc, :v_balance_currency, :v_balance_money, :v_card_type_id, :v_card_type_name, :v_consumption_type, :v_consume_id, :v_consume_name, :v_demoarea, :v_recordid, :v_payment_type_id)", params); 
        
        print("Finish inserting data to Oracle")
        cursor.close();               
        conn.commit();  
        conn.close();  
        
