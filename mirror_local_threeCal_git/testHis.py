import re
import statistics
import drawFig
from datetime import datetime
import numpy
import os

isDebug = True
isTestFig = False
isOutFig = False


def covertTofloat(alist):
    n_alist = list()
    for i in range(len(alist)):
        n_alist.append(float(alist[i]))
    return n_alist

def listProcess(data,dataType):
    del_str = dataType + '='
    line = data.replace(del_str, '')
    line = re.sub('[\[\] \']', '', line)
    tList = line.split(',')
    if not 'date' in dataType and len(tList) > 1:
        tList = covertTofloat(tList)

    return tList

def hisFilterMacdD(macdList,dateList,c_p,num):
    startIndex = ''
    endIndex = ''
    his_list = list()
    for i in range(len(macdList)):
        if macdList[i] <= 0.015 and startIndex =='':
            startIndex = i
        elif startIndex != '' and macdList[i] > 0.015:
            endIndex = i
            di = {}
            di['startIndex'] = startIndex
            di['endIndex'] = endIndex
            his_list.append(di)
            #print("startIndex=",startIndex, ', startDate=', dateList[startIndex], ", endIndex=", endIndex, ', endDate=',dateList[endIndex])
            #print(di)
            startIndex = ''
    percent = hisFilterMacdD_2(his_list,macdList,dateList,c_p,num)
    return percent

def hisFilterMacdD_2(macdDis,macdList,dateList,c_p,num):
    if isDebug: print(macdDis[0])
    if len(macdDis) > 0:
        for i in range(len(macdDis)):
            count_2 = 0
            startIndex =macdDis[i]['startIndex']
            endIndex = macdDis[i]['endIndex']
            length = endIndex - startIndex
            for k in range(length):
                if ((startIndex + k) - 1) > 0 and ((startIndex + k) + 1) <= endIndex:
                    #print('k-1=',(startIndex + k) - 1,', k=',startIndex + k, ', k+1=', (startIndex + k) + 1)
                    if macdList[(startIndex + k) - 1] >= macdList[startIndex + k] and macdList[startIndex + k] <= macdList[(startIndex + k) + 1]:
                        count_2 += 1
            if isDebug: print(macdDis[i], ', count=',count_2)
            macdDis[i]['count_'] = count_2
            if isDebug: print(macdDis[i])
            if isDebug: print('=====\n')
    percent = hisFilterMacdD_3(macdDis,dateList,macdList,c_p,num)
    return percent


def hisFilterMacdD_3(macdDis,dateList,macdList,c_p,num):
    fmacdDisL = list()
    for i in range(len(macdDis)):
        if macdDis[i]['count_'] > 2:
            fmacdDisL.append(macdDis[i])
            if isDebug: print('filter3=',macdDis[i], ', startDate=',dateList[macdDis[i]['startIndex']], ', endDate=',dateList[macdDis[i]['endIndex']])
    percent = hisFilterMacdD_4(fmacdDisL,macdList,dateList,c_p,num)
    return percent

#最后一个峰值peak, 和下一天的差距
def hisFilterMacdD_4(fmacdDisL,macdlist,dateList,c_p,num):
    f4macdDisL = list()
    for i in range(len(fmacdDisL)):
        indexList = list()
        ffmacdlist = list()

        starIndex = fmacdDisL[i]['startIndex']
        endIndex = fmacdDisL[i]['endIndex']
        length = endIndex - starIndex
        for k in range(length):
            if (starIndex + k) - 1 > 0 and (starIndex + k) + 1 < len(macdlist):
                if macdlist[(starIndex + k) - 1] >= macdlist[starIndex + k] and macdlist[starIndex + k] <= macdlist[(starIndex + k) + 1]:
                    indexList.append(starIndex+k)
                    ffmacdlist.append(macdlist[starIndex+k])


        lastindexx = indexList[0]
        meanV = numpy.mean(ffmacdlist)
        lastV = ffmacdlist[0]
        #print(ffmacdlist)
        if lastV < meanV:
            if isDebug: print('hisFilterMacdD_4 date=',dateList[lastindexx])
            f4macdDisL.append(fmacdDisL[i])
    percent = hisFilterMacdD_5(f4macdDisL,macdlist,dateList,c_p,num)
    return percent



def hisFilterMacdD_5(f4macdDisL,macdlist,dateList,c_p,num):
    count_ = 0
    count_1 = 0
    isTotxt = False
    toTxtData = ''
    for i in range(len(f4macdDisL)):
        count_ += 1
        starIndex = f4macdDisL[i]['startIndex']
        endIndex = f4macdDisL[i]['endIndex']
        length = endIndex - starIndex
        lastIndex = ''
        for k in range(length):
            if (starIndex + k) - 1 > 0 and (starIndex + k) + 1 < len(macdlist):
                if macdlist[(starIndex + k) - 1] >= macdlist[starIndex + k] and macdlist[starIndex + k] <= macdlist[
                    (starIndex + k) + 1]:
                    if isDebug: print(starIndex + k, ', date=',dateList[starIndex + k])
                    lastIndex = starIndex + k
                    break
        #print(lastIndex)
        lastIndex_1 = lastIndex
        while lastIndex_1 >= 1 and macdlist[lastIndex_1] <= 0.015:
            lastIndex_1 = lastIndex_1 - 1
        if isDebug: print('lastIndex=',lastIndex,', date=',dateList[lastIndex],', c_p=', c_p[lastIndex], ', lastIndex_1=',lastIndex_1,', macd=',macdlist[lastIndex_1],', c_p=',c_p[lastIndex_1])
        if '2021-09' in dateList[lastIndex]:
            print('num=',num,',date=',dateList[lastIndex])
            isTotxt = True
            toTxtData = 'num=' + num + ',date=' + dateList[lastIndex]
        if round(((c_p[lastIndex_1] - c_p[lastIndex]) / c_p[lastIndex]),2) > 0:
            count_1 += 1
    percent = 0
    if count_1 != 0 and count_ != 0:
        percent = round((count_1/count_),2)
        print('num=', num, ', up ',round((count_1/count_),2),'%')
    else:
        print('num=', num, ', up 0 %')
    if isTotxt and not isDebug:
        toTxtData = toTxtData + ', up ' + str(round((count_1/count_),2)) + '% \n'
        outputToTxt(toTxtData,'./filterResult.txt')
        if isTestFig:
            global isOutFig
            isOutFig = True
    return percent


def outputToTxt(data,filename='./default_output.txt'):
    op = open(filename,'a+')
    op.write(data)
    op.close()

def checkSameMacd(macdList,dateL,c_p):
    for i in range(len(macdList)):
        diff = 999
        if (i+1) < len(macdList):
            if macdList[i] - macdList[i + 1] == 0:
                diffMacd = 0
            else:
                diffMacd = abs(round(((macdList[i] - macdList[i + 1])/macdList[i]),4))

            if diffMacd < 0.01:
                print(dateL[i], 'c_p=',c_p[i],'c_p[i-2]=',c_p[i-2])






def getAlldata(UpDown,stdLimit,drawFigure,priceLimit):
    global isOutFig
    figDirName = 'hisBBands'
    curDate = datetime.now().strftime("%Y%m%d")
    typeName = "macdpi"
    AllfileName = './txtFile/testAldata_' + str(curDate) +'.txt'
    isPause = False
    count_ = 0
    count_1 = 0
    count_2 = 0

    bList = ''
    h_p = ''
    l_p = ''
    c_p = ''
    o_p = ''

    dateL = ''

    h_v = ''
    m_v = ''
    l_v = ''

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
            if isDebug:
                if num != '9943':
                    continue
            del_str = typeName + '='
            line = line.replace(del_str, '')
            line = re.sub('[\[\] ]', '', line)
            all_list = line.split(',')
            #print("xxx=",all_list)
            if len(all_list) > 1:
                all_list = covertTofloat(all_list)
                count_1 += 1
                #main fun
                #percent = hisFilterMacdD(all_list,dateL,c_p,num)
                #test other
                percent = 0
                checkSameMacd(all_list,dateL,c_p)

                if percent > 0.5:
                    count_2 += 1
                if isTestFig:
                    if isOutFig:
                        drawFig.testDraw2Fig(num, all_list, bList, h_p, l_p, c_p, o_p, h_v, m_v, l_v, figDirName)
                        isOutFig = False
                if isDebug:
                    isPause = True


        if isPause:
            break

    txt_open.close()
    if count_1 > 0 and count_2 > 0:
        print('useful ', round((count_2/count_1),2))

    #print('count_=', count_)
    if count_ < 10 and stdLimit > 0.05 and not isPause and isDebug:
        #print('count_=',count_,', stdimit=',stdLimit,', isPause=',isPause,', isDebug=',isDebug)
        #os.system("pause")
        getAlldata(UpDown,round((stdLimit-0.1),2),drawFigure,priceLimit)

getAlldata('down',0.1,True,9999)