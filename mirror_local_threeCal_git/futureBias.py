import read_txt
import math

isDebug = False

class calFuture():
    def cal_36(self,close_p):
        list_36 = list()
        for i in range(len(close_p)):
            if (i + 6) <= len(close_p):
                value_36 = self.three_six_func(close_p[i], close_p[i + 1], close_p[i + 2], close_p[i + 3], close_p[i + 4],
                                          close_p[i + 5])
                list_36.append(value_36)
        return list_36

    def three_six_func(self,p1, p2, p3, p4, p5, p6):
        three_2 = math.floor(((p1 + p2 + p3) / 3) * 10000)
        three_3 = three_2 / 10000
        three_v1 = math.floor(((p1 - three_3) / three_3) * 10000)
        three_v2 = three_v1 / 10000

        six_2 = math.floor(((p1 + p2 + p3 + p4 + p5 + p6) / 6) * 10000)
        six_3 = six_2 / 10000
        six_v1 = math.floor(((p1 - six_3) / six_3) * 10000)
        six_v2 = six_v1 / 10000
        three_six = three_v2 - six_v2
        three_six_1 = round(three_six * 100, 2)
        return three_six_1

    def futureList(self,c_p):
        hightL = list()
        midL = list()
        lowL = list()
        for i in range(len(c_p)):
            if i == 0:
                hightP = c_p[0] + round((c_p[0] / 10), 2)
                midP = c_p[0]
                lowP = c_p[0] - round((c_p[0] / 10), 2)
                print('hightP=',hightP,', midP=',midP,', lowP=',lowP)
                hightL.append(hightP)
                midL.append(midP)
                lowL.append(lowP)
            else:
                hightL.append(c_p[i-1])
                midL.append(c_p[i-1])
                lowL.append(c_p[i-1])
        if isDebug: print("hightL=",hightL)
        if isDebug: print("midL=", midL)
        if isDebug: print("lowL=", lowL)

        h_bias = self.cal_36(hightL)
        m_bias = self.cal_36(midL)
        l_bias = self.cal_36(lowL)

        return h_bias, m_bias, l_bias

    def addTodayCp(self,c_p,tdCp=''):
        newC_p = list()
        if tdCp != '':
            for i in range(len(c_p)):
                if i == 0:
                    newC_p.append(tdCp)
                else:
                    newC_p.append(c_p[i-1])
        else:
            newC_p = c_p
        return newC_p






class singleTestData():

    def local_data(self,data_type, fileName):
        file = './txtFile/' + fileName + '.txt'
        data_list = read_txt.get_list_fTxt(data_type, file)
        return data_list

    def test(self):
        c_p = self.local_data('close_list', 'testData')
        return c_p


if __name__ == '__main__':
    a = singleTestData()
    closeList = a.test()
    print(closeList)
    b = calFuture()
    biasList = b.cal_36(closeList)
    print('bias list=', biasList)

    b.futureList(closeList)

