# coding: UTF-8
import Queue
import traceback
from time import sleep
import thread

import threading
import time

from decimal import Decimal

from bit.chbtcApi import chbtc_api
from weixinWarning import send_msg
from szzcApi import *

# ACCESS KEY
# oV5jPLJxEg2XindDkYVRc5uyWtO6pMzQxE5b9q8X
# SECRET KEY
# 9xbffU5X7FIOVjDrwi8iHKRM7XdMR1cqiD410DLD
from yunbi.client import Client, get_api_path


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter, market):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.market = market

    def run(self):
        # print "Starting " + self.name
        # 获得锁，成功获得锁定后返回True
        # 可选的timeout参数不填时将一直阻塞直到获得锁定
        # 否则超时后将返回False
        threadLock.acquire()
        print_time(self.name, self.counter, 3, self.market)
        # 释放锁
        threadLock.release()


def print_time(threadName, delay, counter, market):
    # while counter:
    time.sleep(delay)
    result = {'yuna': [0, 0], 'yunb': [0, 0], 'sza': [0, 0], 'szb': [0, 0], 'chbtca': [0, 0], 'chbtcb': [0, 0]}
    # getAB(result, market.upper())
    getYunAB(result, market)
    getchbtcAB(result, market)

    for key in result:
        if key.count('sz'):
            result[key][0] = (result[key][0] / float(100))
            result[key][1] = (result[key][1] / float(100000))

    # print 'result', result
    # print market

    if float(result['yuna'][0]) > 0 and float(result['yunb'][0]) > 0:

        # arb = float(result['yunb'][0]) - result['sza'][0]

        diff = float(result['yuna'][0]) * 0.01
        arb = float(result['yuna'][0]) * 0.01
        # print float(result['yuna'][0]) * 0.01

        arb = arb * 0.8

        # print arb
        #
        if result['szb'][0] > 0 and result['szb'][0] - float(result['yuna'][0]) > arb:
            arb = result['szb'][0] - float(result['yuna'][0])
            fromTo = '云币买价 %s 量 %s - 海枫藤卖价 %s 量 %s' % (
                str(result['yuna'][0]), str(result['yuna'][1]), str(result['szb'][0]), str(result['szb'][1]))
        else:
            fromTo = '海枫藤买价 %s 量 %s - 云币卖价 %s 量 %s' % (
                str(result['sza'][0]), str(result['sza'][1]), str(result['yunb'][0]), str(result['yunb'][1]))
        # pass
        if market.count('et'):
            members = client.get(get_api_path('members'))
            account = api.query_account()
            if members is not None and account is not None:
                YB_cny = float(members['accounts'][0]['balance'])
                CN_cny = account['result']['balance']['CNY']['amount']
                YB_amt = 0
                CN_amt = 0
                if market[0:3] == 'eth':
                    YB_amt = float(members['accounts'][11]['balance'])
                    CN_amt = account['result']['balance'][market[0:3].upper()]['amount']
                    print YB_cny
                    print YB_amt
                    print CN_cny
                    print CN_amt
                    print CN_amt + YB_amt
            # print market[0:3]
            if result['chbtcb'][0] - float(result['yuna'][0]) > arb:

                diff = result['chbtcb'][0] - float(result['yuna'][0])
                rage = round(diff / result['yuna'][0] * 10, 3)
                # print 'rage', rage
                fromTo = '云币买价 %s 量 %s - CHBTC卖价 %s 量 %s' % (
                    str(result['yuna'][0]), str(result['yuna'][1]), str(result['chbtcb'][0]), str(result['chbtcb'][1]))
                # if market[0:3] == 'eth':
                #     YB_cny = float(members['accounts'][0]['balance'])
                #     YB_eth = float(members['accounts'][11]['balance'])
                #     CN_cny = account['result']['balance']['CNY']['amount']
                #     CN_eth = account['result']['balance'][market[0:3].upper()]['amount']
                #     print YB_cny
                #     print YB_eth
                #     print CN_cny
                #     print CN_eth
                #     print CN_eth + YB_eth

                if CN_amt > 2:
                    # buy 10 dogecoins at price 0.001
                    params = {'market': market, 'side': 'buy', 'volume': rage, 'price': result['yuna'][0]}
                    res = client.post(get_api_path('orders'), params)
                    print res
                    print api.order(str(result['chbtcb'][0]), str(rage), '0', market[0:3])
                    cnOrder = api.order(str(result['chbtcb'][0]), str(rage), '0', market[0:3])
                    if cnOrder['code'] == 1000:
                        pass
                    print cnOrder

                    # print members['accounts'][0]
                    # print members['accounts'][11]
                    #
                    # print account['result']['balance']['CNY']['amount']
                    # print account['result']['balance'][market[0:3].upper()]['amount']
                    # print account['result']['balance'][market[0:3].upper()]['amount'] + \
                    #       members['accounts'][11]['balance']
                    print 'arb : ', arb, ' ; diff :', diff

            elif float(result['sza'][0]) > 0 and result['chbtcb'][0] - float(result['sza'][0]) > 2:
                diff = result['chbtcb'][0] - result['sza'][0]
                fromTo = '海枫藤买价 %s 量 %s - CHBTC卖价 %s 量 %s' % (
                    str(result['sza'][0]), str(result['sza'][1]), str(result['chbtcb'][0]), str(result['chbtcb'][1]))
            elif result['szb'][0] > 0 and result['szb'][0] - float(result['chbtca'][0]) > arb:
                diff = result['szb'][0] - result['chbtca'][0]
                fromTo = 'CHBTC买价 %s 量 %s - 海枫藤卖价 %s 量 %s' % (
                    str(result['chbtca'][0]), str(result['chbtca'][1]), str(result['szb'][0]), str(result['szb'][1]))
            elif float(result['yunb'][0]) - result['chbtca'][0] > arb:
                diff = float(result['yunb'][0]) - result['chbtca'][0]
                rage = round(diff / result['chbtca'][0] * 10, 3)

                fromTo = 'CHBTC买价 %s 量 %s - 云币卖价 %s 量 %s' % (
                    str(result['chbtca'][0]), str(result['chbtca'][1]), str(result['yunb'][0]), str(result['yunb'][1]))

                if YB_amt > 2:
                    cnOrder = api.order(str(result['chbtca'][0]), str(rage), '1', market[0:3])
                    if cnOrder is not None:
                        if cnOrder['code'] == 1000:
                            # sell 10 dogecoins at price 0.01
                            params = {'market': market, 'side': 'sell', 'volume': rage, 'price': result['yunb'][0]}
                            res = client.post(get_api_path('orders'), params)
                            print res
                            print res['id']
                            # print res['code']
                            print 'rage', rage
                            print cnOrder
                    # print members['accounts'][0]
                    # print members['accounts'][11]['balance']
                    # #
                    # print account['result']['balance']['CNY']['amount']
                    # print account['result']['balance'][market[0:3].upper()]['amount']
                    # print account['result']['balance'][market[0:3].upper()]['amount'] + float(members['accounts'][11]['balance'])
                    print 'arb : ', arb, ' ; diff :', diff

        # print members['accounts'][0]
        # print members['accounts'][11]
        # #
        # print account['result']['balance']['CNY']['amount']
        # print account['result']['balance'][market[0:3].upper()]['amount']
        # if(account['result']['balance'][market[0:3].upper()]['amount']):
        #
        # print account['result']['balance'][market[0:3].upper()]['amount']
        # print account['result']

        # print 'arb : ', arb, ' ; diff :', diff
        if arb > diff:
            send_msg('4',
                     '''%s 套利空间 : %s : %s  : %s : %s''' % (
                         market.upper(), fromTo, arb, rage, time.asctime(time.localtime(time.time()))))
            sleep(30)
        else:
            ''''''
            sleep(1)
    sleep(0.5)
    # print "%s: %s" % (threadName, time.ctime(time.time()))
    # counter -= 1


if __name__ == '__main__':
    access_key = '2f852bcc-3af0-4b6c-b0a5-e8802bfc4b1b'
    access_secret = '18ebc9cb-f8b8-4de0-a6a1-02a0d1de93a0'
    api = chbtc_api(access_key, access_secret)

    client = Client(access_key='oV5jPLJxEg2XindDkYVRc5uyWtO6pMzQxE5b9q8X',
                    secret_key='9xbffU5X7FIOVjDrwi8iHKRM7XdMR1cqiD410DLD')

    while True:

        threadLock = threading.Lock()
        threads = []

        # 创建新线程
        # thread1 = myThread(1, "Thread-1", 1, 'zeccny', )
        # 添加线程到线程列表
        # threads.append(thread1)

        thread2 = myThread(2, "Thread-2", 2, 'ethcny', )
        threads.append(thread2)

        # thread3 = myThread(3, "Thread-3", 3, 'etccny', )
        # threads.append(thread3)

        # 等待所有线程完成
        for t in threads:
            # 开启新线程
            # thread1.start()
            # thread2.start()
            # thread3.start()
            t.setDaemon(True)
            t.start()
        t.join()
        # print "Exiting Main Thread"
