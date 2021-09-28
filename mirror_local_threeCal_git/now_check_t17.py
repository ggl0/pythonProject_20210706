import re
import statistics
import drawFig
from datetime import datetime

def covertTofloat(alist):
    n_alist = list()
    for i in range(len(alist)):
        n_alist.append(float(alist[i]))
    return n_alist

######################Down filter########################
def filterMacdD_1(macdList,startIndex=2):
    count_ = 0
    for i in range(len(macdList)):
        if (i + startIndex) < len(macdList):
            if (i < startIndex and macdList[i] > 0) or (macdList[i] <= 0.015):
                count_ += 1
            else:
                break
        else:
            break
    return count_

def filterMacdD_2(macdList,count_,dateL):
    count_2 = 0
    for i in range(count_):
        if (i - 1) >= 0 and (i + 1) < count_:
            if macdList[i - 1] >= macdList[i] and macdList[i] <= macdList[i + 1]:
                count_2 += 1
    #newList = list()
    #newList = macdList[0:count_]
    #print(statistics.stdev(newList))
    return count_2
##########################################################

######################Up filter########################
def filterMacdU_1(macdList,startIndex=0):
    count_ = 0
    for i in range(len(macdList)):
        if (i < startIndex and macdList[i] < 0) or (macdList[i] >= -0.015):
            count_ += 1
        else:
            break
    return count_

def filterMacdU_2(macdList,count_,dateL):
    count_2 = 0
    for i in range(count_):
        if (i - 1) >= 0 and (i + 1) < count_:
            if macdList[i - 1] <= macdList[i] and macdList[i] >= macdList[i + 1]:
                count_2 += 1
    return count_2
##########################################################

def calStd(macdList,count_):
    newList = list()
    newList = macdList[0:count_]
    std_ = statistics.stdev(newList)
    return std_

def listProcess(data,dataType):
    del_str = dataType + '='
    line = data.replace(del_str, '')
    line = re.sub('[\[\] ]', '', line)
    tList = line.split(',')
    if not 'date' in dataType and len(tList) > 1:
        tList = covertTofloat(tList)
    return tList

def checkPrice(h_p,l_p,m_v):
    if l_p >= m_v or h_p >= m_v >= l_p:
        return True
    return False




def getAlldata(UpDown,stdLimit,drawFigure,priceLimit):
    curDate = datetime.now().strftime("%Y%m%d")
    typeName = "macdpi"
    AllfileName = './txtFile/testAldata_' + str(curDate) +'.txt'
    isPause = False
    count_ = 0

    bList = ''
    h_p = ''
    l_p = ''
    c_p = ''
    o_p = ''

    dateL = ''

    h_v = ''
    m_v = ''
    l_v = ''

    figDirName = 'BBands_' + UpDown



    print('stdLimit=',stdLimit)
    txt_open = open(AllfileName)
    lines = txt_open.readlines()
    for line in lines:
        all_list = ''

        line = line.strip('\n')
        if "-----------------" in line:
            num = re.sub('[\[\] -]','',line)
            #print(num)
        if 'high_list' in line:
            if h_p != '':
                h_p = ''
            h_p = listProcess(line,'high_list')
        if 'low_list' in line:
            if l_p != '':
                l_p = ''
            l_p = listProcess(line,'low_list')
        if 'close_list' in line:
            if c_p != '':
                c_p = ''
            c_p = listProcess(line,'close_list')
        if 'open_list' in line:
            if o_p != '':
                o_p = ''
            o_p = listProcess(line,'open_list')

        if 'date_list' in line:
            if dateL != '':
                dateL = ''
            dateL = listProcess(line,'date_list')

        if 'H_v' in line:
            if h_v != '':
                h_v = ''
            h_v = listProcess(line,'H_v')
        if 'M_v' in line:
            if m_v != '':
                m_v = ''
            m_v = listProcess(line,'M_v')
        if 'L_v' in line:
            if l_v != '':
                l_v = ''
            l_v = listProcess(line,'L_v')

        if 'bias_list' in line:
            if bList != '':
                bList = ''
            bList = listProcess(line,'bias_list')



        if typeName in line:
            del_str = typeName + '='
            line = line.replace(del_str, '')
            line = re.sub('[\[\] ]', '', line)
            all_list = line.split(',')
            #print("xxx=",all_list)
            if not 'date' in typeName and len(all_list) > 1:
                all_list = covertTofloat(all_list)
                down_count = 0
                #print(all_list)
                #isPause = True
                if UpDown == 'down':
                    down_count = filterMacdD_1(all_list)
                else:
                    down_count = filterMacdU_1(all_list)
                if down_count > 10:
                    #if num == '8476': print("check num=",num,", count=",down_count)
                    count_2 = 0
                    if UpDown == 'down':
                        count_2 = filterMacdD_2(all_list,down_count,dateL)
                        #print("check1 num=", num, ", count=", down_count, ', count_2=', count_2)
                    else:
                        count_2 = filterMacdU_2(all_list, down_count,dateL)
                    if count_2 > 2:
                        #count_ += 1
                        #if num == '8476': print("check1 num=", num, ", count=", down_count, ', count_2=',count_2)
                        std = calStd(all_list,down_count)
                        if std > stdLimit:
                            if float(c_p[0]) < priceLimit and checkPrice(h_p,l_p,m_v):
                                count_ += 1
                                print("check2 num=", num, ", count=", down_count, ', count_2=', count_2, ', std=',std, ', c_p_today=',c_p[0])
                                #print('bList=',bList)
                                if drawFigure:
                                    drawFig.testDraw2Fig(num,all_list,bList,h_p,l_p,c_p,o_p,h_v,m_v,l_v,figDirName)
                                isPause = False
        if isPause:
            break

    txt_open.close()

    print('count_=', count_)
    if count_ < 10 and stdLimit > 0.05 and not isPause:
        getAlldata(UpDown,round((stdLimit-0.1),2),drawFigure,priceLimit)

# priceLimit=9999最大, 参数1: 输入up or down
getAlldata('down',0.0,True,9999)