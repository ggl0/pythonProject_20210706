import read_txt
import matplotlib.pyplot as plt
import mpl_finance as mpf
from matplotlib.font_manager import FontProperties

import futureBias

isDebug = True


def local_data(data_type, fileName):
    file = './txtFile/' + fileName + '.txt'
    data_list = read_txt.get_list_fTxt(data_type, file)
    return data_list

def drawBar(plt,xList,yList,type):
    days = list()
    for i in range(xList):
        days.append(i)

    #plt.figure(figsize=(15,10),dpi=50,linewidth = 2)
    for i in range(len(yList)):
        if yList[i] >= 0:
            plt.bar(days[i], yList[i], 1, color="red", edgecolor="black")
        else:
            plt.bar(days[i], yList[i], 1, color="green", edgecolor="black")

    #dplt = plt.legend(loc = "best", fontsize=20)
    return plt

def drawLine(plt,xList,yList,type):
    #print('xList len=',xList,', yList len=', len(yList))
    days = list()
    for i in range(xList):
        days.append(i)

    #plt.figure(figsize=(15,10),dpi=50,linewidth = 2)
    plt.plot(days,yList,'s-',color = 'r')
    plt.axhline(y=0, xmin=0, xmax=xList)

    #dplt = plt.legend(loc = "best", fontsize=20)
    return plt




def macdType(plt,searchDate,figNumY,figNumX,figSeq,macdpi=''):
    plt.subplot(figNumY, figNumX, figSeq)
    length = 60

    #local data
    if macdpi == '':
        macdpi = local_data('macdpi', 'testData')
        date = local_data('date_list', 'testData')
        start_index = 0
        if searchDate != 0:
            searchDate = "'" + searchDate + "'"
            start_index = date.index(searchDate)
        #print(start_index)

        macdpi = macdpi[start_index:(start_index+length)]
        date = date[start_index:(start_index+length)]
        #print(date)
        #print(len(date))
    else:
        macdpi = macdpi[0:length]

    pPlt = drawBar(plt,length,macdpi,'macd')
    return pPlt

def biasType(plt,searchDate,figNumY,figNumX,figSeq,biasLi=''):
    plt.subplot(figNumY, figNumX, figSeq)
    length = 60

    if biasLi == '':
        biasLi = local_data('bias_list', 'testData')
        date = local_data('date_list', 'testData')

        start_index = 0

        if searchDate != 0:
            searchDate = "'" + searchDate + "'"
            start_index = date.index(searchDate)
        #print(start_index)

        biasLi = biasLi[start_index:(start_index+length)]
        date = date[start_index:(start_index+length)]
        #print(date)
        #print(len(date))
    else:
        biasLi = biasLi[0:length]

    pPlt = drawLine(plt,length,biasLi,'bias')
    return pPlt

# k line and BBands type
def kAbbType(plt,searchDate,figNumY,figNumX,figSeq,highLi='',lowLi='',closeLi='',openLi='',HvLi='',MvLi='',LvLi=''):
    font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=20)

    ax = plt.subplot(figNumY, figNumX, figSeq)
    length = 60
    if highLi == '':
        highLi = local_data('high_list', 'testData')
        lowLi = local_data('low_list', 'testData')
        closeLi = local_data('close_list', 'testData')
        openLi = local_data('open_list', 'testData')

        HvLi = local_data('H_v', 'testData')
        MvLi = local_data('M_v', 'testData')
        LvLi = local_data('L_v', 'testData')

        date = local_data('date_list', 'testData')

        start_index = 0

        if searchDate != 0:
            searchDate = "'" + searchDate + "'"
            start_index = date.index(searchDate)
        #print(start_index)

        highLi = highLi[start_index:(start_index+length)]
        lowLi = lowLi[start_index:(start_index + length)]
        closeLi = closeLi[start_index:(start_index + length)]
        openLi = openLi[start_index:(start_index + length)]

        HvLi = HvLi[start_index:(start_index + length)]
        MvLi = MvLi[start_index:(start_index + length)]
        LvLi = LvLi[start_index:(start_index + length)]

        date = date[start_index:(start_index+length)]
    else:
        highLi = highLi[0:length]
        lowLi = lowLi[0:length]
        closeLi = closeLi[0:length]
        openLi = openLi[0:length]

        HvLi = HvLi[0:length]
        MvLi = MvLi[0:length]
        LvLi = LvLi[0:length]

    x_number = range(len(HvLi))

    #pPlt = drawLine(plt,length,biasLi)
    mpf.candlestick2_ochl(ax, openLi, closeLi, highLi, lowLi, width=0.1, colorup='r', colordown='green')

    for i in range(len(HvLi)):
        # high
        plt.plot(x_number,  # x轴数据
                 HvLi,  # y轴数据
                 # linestyle = '--', # 折线类型
                 marker='o',
                 linewidth=0.5,  # 折线宽度
                 markersize=2,  # 点的大小
                 )
        # med
        plt.plot(x_number,  # x轴数据
                 MvLi,  # y轴数据
                 # linestyle = '--', # 折线类型
                 marker='o',
                 linewidth=0.5,  # 折线宽度
                 markersize=2,  # 点的大小
                 )
        # low
        plt.plot(x_number,  # x轴数据
                 LvLi,  # y轴数据
                 # linestyle = '--', # 折线类型
                 marker='o',
                 linewidth=0.5,  # 折线宽度
                 markersize=2,  # 点的大小
                 )
    '''
    for a, b in zip(x_number, HvLi):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=8)
    for a, b in zip(x_number, MvLi):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=8)
    for a, b in zip(x_number, LvLi):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=8)
    '''

    plt.xlabel(u'10天布林通道数据', fontproperties=font_set)


    plt.grid() #背景格纹

    #print('highLi=',ax)
    #plt.show()
    #del ax
    return plt


def testDraw1Fig():
    plt.figure(figsize=(20, 12), dpi=50, linewidth=2)
    biasType(plt,0,1,1,1)
    #macdType(plt,0,1,1,1)
    #kAbbType(plt,0,1,1,1)
    plt.show()

def testDraw2Fig(num='',macdpi='',biasList='',highLi='',lowLi='',closeLi='',openLi='',HvLi='',MvLi='',LvLi='',fileName='BBands'):
    plt.figure(figsize=(15, 10), dpi=50, linewidth=2)
    #macdType(plt,0,3,1,1)
    #biasType(plt,0,3,1,2)
    #kAbbType(plt,0,3,1,3)
    if num == '':
        macdType(plt, 0, 3, 1, 1)
        biasType(plt, 0, 3, 1, 2)
        kAbbType(plt, 0, 3, 1, 3)
        plt.show()
    else:
        #print("num=", num, ", macdpi=", macdpi)
        macdType(plt, 0, 3, 1, 1,macdpi)
        biasType(plt, 0, 3, 1, 2,biasList)
        kAbbType(plt, 0, 3, 1, 3,highLi,lowLi,closeLi,openLi,HvLi,MvLi,LvLi)
        plt.savefig(fileName + '/' + str(num) + '.png')
        plt.clf()
        plt.close()


#draw bias future line
def drawBiasFLine(plt):
    fbiasC_p = futureBias.singleTestData()
    fbias = futureBias.calFuture()

    c_p = fbiasC_p.test()
    c_p = fbias.addTodayCp(c_p,50.90)
    if isDebug: print('c_p=', c_p)
    hBiasL,mBiasL,lBiasL = fbias.futureList(c_p)

    hBiasL = hBiasL[0:60]
    mBiasL = mBiasL[0:60]
    lBiasL = lBiasL[0:60]

    if isDebug: print('hBiasL[0]=',hBiasL[0])
    if isDebug: print('mBiasL[0]=', mBiasL[0])
    if isDebug: print('lBiasL[0]=', lBiasL[0])


    limit = 60

    days = list()
    for i in range(limit):
        days.append(i)

    plt.plot(days,hBiasL,'s-',color = 'r')
    plt.plot(days, mBiasL, 's-', color='g')
    plt.plot(days, lBiasL, 's-', color='b')

    plt.axhline(y=0, xmin=0, xmax=limit)

    return plt

def testDrawBiasFFig():
    plt.figure(figsize=(20, 12), dpi=50, linewidth=2)
    drawBiasFLine(plt)
    #macdType(plt,0,1,1,1)
    #kAbbType(plt,0,1,1,1)
    plt.show()

if __name__ == '__main__':
    #testDraw2Fig()
    #testDraw1Fig()
    testDrawBiasFFig()
