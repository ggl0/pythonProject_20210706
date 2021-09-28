import All_number
import mysql.connector
import sys
import datetime

import BBands
import BIAS_v0

isDebug = True
logErrorTag = 'dbToTxt_Error'

def setDate(dateNow=datetime.datetime.now().strftime('%Y%m%d')):
    return str(dateNow)


def db_connect():
    connection = mysql.connector.connect(
        host='127.0.0.1',          # 主機名稱
        user='root',        # 帳號
        password='cba2@GHJ')  # 密碼
    return connection

def transDBdate():
    dateStr = 'CAST(`date` AS CHAR)'
    return dateStr

def procDataTypeL(dataTypeL):
    dbStr = ''
    for i in range(len(dataTypeL)):
        spStr = ''
        if dataTypeL[i] == 'date':
            spStr = transDBdate()
        else:
            spStr = '`' + dataTypeL[i] + '`'
        dbStr= dbStr + spStr
        if i != (len(dataTypeL) - 1):
            dbStr = dbStr + ','
    if isDebug: print(dbStr)
    return dbStr


def getDBdata(num,dbName,dataTypeL):
    if isDebug: print('num=',num,', dataTypeL=',dataTypeL)
    dbCommand = 'SELECT ' + procDataTypeL(dataTypeL) +' From `' + num + '` Order by `date` DESC;'

    connection = db_connect()
    if connection.is_connected():
        cursor = connection.cursor()
        u_database_c = "use " + dbName + ";"
        cursor.execute(u_database_c)
        try:
            cursor.execute(dbCommand)
            all_data = cursor.fetchall()
        except Exception as e:
            print('get_price_allandDate has some error! e=', str(e))
            all_data = ''
        cursor.close()
        connection.close()
    if isDebug: print(all_data[0])
    return all_data

def procBBands(closeList,writeTXT):
    H_v, M_v, L_v = BBands.main(closeList)
    H_vStr = 'H_v=' + str(H_v) + '\n'
    M_vStr = 'M_v=' + str(M_v) + '\n'
    L_vStr = 'L_v=' + str(L_v) + '\n'
    writeTXT.write(H_vStr)
    writeTXT.write(M_vStr)
    writeTXT.write(L_vStr)
    del H_v,M_v,L_v,H_vStr,M_vStr,L_vStr

def procBIAS(closeList,writeTXT):
    BIAS_36 = BIAS_v0.cal_36(closeList)
    biasStr = 'bias_list=' + str(BIAS_36) + '\n'
    writeTXT.write(biasStr)
    del BIAS_36,biasStr

def writeDBToTxt(dataType,allDataL,fileName):
    for i in range(len(dataType)):
        locals()[dataType[i] + '_List'] = list()
    #print(locals())

    for j in range(len(allDataL)):
        for k in range(len(dataType)):
            locals()[dataType[k] + '_List'].append(allDataL[j][k])
    if isDebug: print(locals()[dataType[0] + '_List'][len(allDataL) - 1])
    if isDebug: print(locals()[dataType[1] + '_List'][len(allDataL) - 1])
    if isDebug: print(locals()[dataType[2] + '_List'][len(allDataL) - 1])
    if isDebug: print(locals()[dataType[3] + '_List'][len(allDataL) - 1])
    if isDebug: print(locals()[dataType[4] + '_List'][len(allDataL) - 1])

    write_log = open(fileName, 'a', encoding='UTF-8')
    for l in range(len(dataType)):
        wrStr = dataType[l] + '=' + str(locals()[dataType[l] + '_List']) + '\n'
        write_log.write(wrStr)
        if dataType[l] == 'close_p':
            procBBands(locals()[dataType[l] + '_List'], write_log)
            procBIAS(locals()[dataType[l] + '_List'], write_log)
        del locals()[dataType[l] + '_List']
    write_log.close()
	#del allDataL


def writeTxt(dataStr,fileName):
    writeStr = open(fileName, 'a', encoding='UTF-8')
    writeStr.write(dataStr)
    writeStr.close()

def main():
    fileName = 'testAldata_' + setDate() + '.txt'
    type = ['twse', 'tpex']
    dataTypeL = ['high_p','low_p','close_p','date','open_p','type1','type2','type7','type8']
    for i in range(len(type)):
        stock_num_list, stock_num_list_type, stock_num_list_public_date = All_number.main(type[i])
        for k in range(len(stock_num_list)):
            try:
                print(stock_num_list[k])
                allDataList = getDBdata(stock_num_list[k],'stock1',dataTypeL)
                writeTxt('-----------------' + str(stock_num_list[k]) + '-----------------' + '\n', fileName)
                writeDBToTxt(dataTypeL,allDataList,fileName)
            except Exception as e:
                if isDebug: print(stock_num_list[k],' has some error! e=',e)
                errorStr = logErrorTag + ': main: ' + str(stock_num_list[k]) + ' has some error! e=' + str(e)
                writeTxt(errorStr,logErrorTag+'.txt')



    clearAllAllocate()

def clearAllAllocate():
    print(locals())
    sys.modules[__name__].__dict__.clear()
    print('After clear')
    print('locals=',locals())

main()