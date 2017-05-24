import json, urllib2, hashlib, struct, sha, time, sys


class chbtc_api:
    def __init__(self, mykey, mysecret):
        self.mykey = mykey
        self.mysecret = mysecret

    def __fill(self, value, lenght, fillByte):
        if len(value) >= lenght:
            return value
        else:
            fillSize = lenght - len(value)
        return value + chr(fillByte) * fillSize

    def __doXOr(self, s, value):
        slist = list(s)
        for index in xrange(len(slist)):
            slist[index] = chr(ord(slist[index]) ^ value)
        return "".join(slist)

    def __hmacSign(self, aValue, aKey):
        keyb = struct.pack("%ds" % len(aKey), aKey)
        value = struct.pack("%ds" % len(aValue), aValue)
        k_ipad = self.__doXOr(keyb, 0x36)
        k_opad = self.__doXOr(keyb, 0x5c)
        k_ipad = self.__fill(k_ipad, 64, 54)
        k_opad = self.__fill(k_opad, 64, 92)
        m = hashlib.md5()
        m.update(k_ipad)
        m.update(value)
        dg = m.digest()

        m = hashlib.md5()
        m.update(k_opad)
        subStr = dg[0:16]
        m.update(subStr)
        dg = m.hexdigest()
        return dg

    def __digest(self, aValue):
        value = struct.pack("%ds" % len(aValue), aValue)
        # print value
        h = sha.new()
        h.update(value)
        dg = h.hexdigest()
        return dg

    def __api_call(self, path, params=''):
        try:
            SHA_secret = self.__digest(self.mysecret)
            sign = self.__hmacSign(params, SHA_secret)
            reqTime = (int)(time.time() * 1000)
            params += '&sign=%s&reqTime=%d' % (sign, reqTime)
            url = 'https://trade.chbtc.com/api/' + path + '?' + params
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=2)
            doc = json.loads(response.read())
            return doc
        except Exception, ex:
            print sys.stderr, 'chbtc request ex: ', ex
            return None

    def query_account(self):
        try:
            params = "method=getAccountInfo&accesskey=" + self.mykey
            path = 'getAccountInfo'

            obj = self.__api_call(path, params)
            # print obj
            return obj
        except Exception, ex:
            print sys.stderr, 'chbtc query_account exception,', ex
            return None

    def order(self, price, amount, tradeType, market):
        try:
            # '''method=order&accesskey=%s&price=%s&amount=%s&tradeType=%s&currency=%s_cny'''
            params = "method=order&accesskey=" + self.mykey + '&price=' + price + '&amount=' + amount + '&tradeType=' + tradeType + '&currency=' + market + '_cny'
            path = 'order'

            obj = self.__api_call(path, params)
            return obj
        except Exception, ex:
            print sys.stderr, 'chbtc query_account exception,', ex
            return None


if __name__ == '__main__':
    access_key = '2f852bcc-3af0-4b6c-b0a5-e8802bfc4b1b'
    access_secret = '18ebc9cb-f8b8-4de0-a6a1-02a0d1de93a0'

    api = chbtc_api(access_key, access_secret)

    print api.query_account()
    print api.order()
