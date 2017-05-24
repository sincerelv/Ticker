from  poloniexAPI import *
from bittrexAPI import *
import requests


#806f019d0ea9a5796d4d09a80581237b

#3rfv5ws43zv7gd9yet5efmthg76km88bmf165dgfqzaqfcxuku4px9

def getAB(result, market):
    try:
        abData = requests.get('https://szzc.com/api/view/depth/%s' % (market))
    except:
        pass
    else:
        # print yunbi.json()['zeccny']['ticker']
        # print yunbide.json()['bids']
        # print yunbide.json()['asks']
        a = b = c = d = 0
        avg = avg1 = 0
        # for len(yunbide.json()['bids'])
        if abData.status_code == 200:

            result['szb'] = abData.json()['bid'][0]
            for bid in abData.json()['bid']:
                # a += float(bid[0])
                # print float(bid[1])/1000000
                b += float(bid[1]) / 1000000
                # print 'a', a, 'b', b
                avg += float(bid[0]) * float(bid[1])
                if b >= 10:
                    # print avg / float(b)/100000000
                    break
            result['sza'] = abData.json()['ask'][0]
            for ask in abData.json()['ask']:
                # c += float(ask[0])
                d += float(ask[1]) / 1000000
                # result['szb'] = float(ask[1])/1000000
                avg1 += float(ask[0]) * float(ask[1])
                # print 'c', c, 'd', d
                if d >= 10:
                    # print avg1 / float(d)/100000000
                    break

        return result


def getYunAB(result, market):
    try:
        # yunbi = requests.get('https://yunbi.com/api/v2/tickers.json')
        yunbide = requests.get('https://yunbi.com//api/v2/depth.json?market=%s&limit=10' % (market))
    except:
        pass
    else:
        # print yunbi.json()['zeccny']['ticker']
        # print yunbide.json()['bids']
        # print yunbide.json()['asks']
        a = b = c = d = 0
        avg = avg1 = 0
        # for len(yunbide.json()['bids'])
        # print yunbide.status_code

        if yunbide.status_code == 200:
            result['yunb'] = yunbide.json()['bids'][0]
            for bid in sorted(yunbide.json()['bids'], key=lambda x: x[1]):
                # a += float(bid[0])
                b += float(bid[1])
                # result['yunb'] = float(bid[1])
                # print 'a', a, 'b', b
                avg += float(bid[0]) * float(bid[1])
                if b >= 10:
                    # print avg / float(b)
                    break
            result['yuna'] = yunbide.json()['asks'][9]
            for ask in sorted(yunbide.json()['asks'], key=lambda x: x[1]):
                # c += float(ask[0])
                d += float(ask[1])
                # result['yuna'] = float(ask[1])
                avg1 += float(ask[0]) * float(ask[1])
                # print 'c', c, 'd', d
                if d >= 10:
                    # print avg1 / float(d)
                    break
        else:
            result['yunb'] = result['szb']
            result['yuna'] = result['sza']



def getchbtcAB(result, market):
    # print market[0:3]
    # print market[-3:]
    # print
    if market.count('zec'):
        return result

    try:
        abData = requests.get('http://api.chbtc.com/data/v1/depth?currency=%s&size=3&merge=0.1' % ('_'.join([market[0:3], market[-3:]])))
    except:
        pass
    else:
        # print yunbi.json()['zeccny']['ticker']
        # print yunbide.json()['bids']
        # print yunbide.json()['asks']
        a = b = c = d = 0
        avg = avg1 = 0
        # for len(yunbide.json()['bids'])
        if abData.status_code == 200:
            # print abData.json()
            result['chbtcb'] = abData.json()['bids'][0]
            for bid in abData.json()['bids']:
                # a += float(bid[0])
                # print float(bid[1])/1000000
                b += float(bid[1]) / 1000000
                # print 'a', a, 'b', b
                avg += float(bid[0]) * float(bid[1])
                if b >= 10:
                    # print avg / float(b)/100000000
                    break
            result['chbtca'] = abData.json()['asks'][2]
            for ask in abData.json()['asks']:
                # c += float(ask[0])
                d += float(ask[1]) / 1000000
                # result['szb'] = float(ask[1])/1000000
                avg1 += float(ask[0]) * float(ask[1])
                # print 'c', c, 'd', d
                if d >= 10:
                    # print avg1 / float(d)/100000000
                    break

        return result


if __name__ == '__main__':
    # getAB('https://szzc.com/api/view/depth/ZECCNY')


    ''''''
