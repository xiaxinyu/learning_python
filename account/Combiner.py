'''
Created on 2018.1.24

@author: summer.xia
@contact: summer_west2010@126.com
'''
dateSpliter = ' '

def findRelatedAlipay(transData, blanceMoney, alipayMatrix):
    for alipay in alipayMatrix:
        date = alipay[2].split(dateSpliter)[0]
        money = alipay[9]
        if date == transData and money == blanceMoney:
            return alipay
    return None
    
def combineCCBAndAlipay(creditMatrix, alipayMatrix):
    creditNone = False   
    if creditMatrix is None or len(creditMatrix) <= 0:
        creditNone = True 
    alipayNone = False  
    if alipayMatrix is None or len(alipayMatrix) <= 0:
        alipayNone = True  
    if creditNone or alipayNone:
        print('can not combine credit and alipay')
    
    rows = []
    for credit in creditMatrix:
        row = credit
        transDate = credit[0].split(dateSpliter)[0]
        blanceMoney = credit[3]
        alipay = findRelatedAlipay(transDate, blanceMoney, alipayMatrix)        
        if alipay is not None:
            row[6] = credit[6] + "@@" + alipay[7] + "@@" + alipay[8]        
        rows.append(row)
    return rows 
        
    
    

    
    