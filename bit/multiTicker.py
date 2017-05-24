# coding: UTF-8

from multiprocessing import Process

from szzcApi import *
from weixinWarning import send_msg


def diffscan(market):
    # print market
    while True:
        result = {'yuna': [0, 0], 'yunb': [0, 0], 'sza': [0, 0], 'szb': [0, 0]}
        getAB(result, market.upper())
        getYunAB(result, market)

        for key in result:
            if key.count('sz'):
                result[key][0] = (result[key][0] / float(100))
                result[key][1] = (result[key][1] / float(100000))
        print 'result', result
        print market
        if market.count('zec'):
            diff = 5
        elif market.count('etc'):
            diff = 0.5
        else:
            diff = 3

        if result['sza'][0] and result['szb'][0] > 0 and result['yuna'][0] > 0 and result['yunb'][0]:

            arb = float(result['yunb'][0]) - result['sza'][0]

            if result['szb'][0] - float(result['yuna'][0]) > arb:
                arb = result['szb'][0] - float(result['yuna'][0])
                fromTo = '云币买价 %s 量 %s - 海枫藤卖价 %s 量 ->价差 ： %s' % (str(result['yuna'][0]), str(result['yuna'][1]), str(result['szb'][0]), str(result['szb'][1]))
            else:
                fromTo = '海枫藤买价 %s 量 %s - 云币卖价 %s 量 ->价差 ：%s' % (str(result['sza'][0]), str(result['sza'][1]), str(result['yunb'][0]), str(result['yunb'][1]))
                # pass

            print 'arb : ', arb, ' ; diff :', diff
            if arb > diff:
                send_msg('4', '''%s 套利空间 : %s : %s ''' % (market.upper(), fromTo, arb))
                time.sleep(600)
            else:
                time.sleep(6)
                # pass


if __name__ == '__main__':
    while True:
        p = Process(target=diffscan, args=('ethcny',))
        p.start()
        p = Process(target=diffscan, args=('zeccny',))
        p.start()
        p = Process(target=diffscan, args=('etccny',))
        p.start()
        p.join()
