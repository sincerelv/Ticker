# encoding: UTF-8

import hashlib
import json
import zlib
from threading import Thread
import websocket
import logging


########################################################################
class OkCoinApi(object):
    """基于Websocket的API对象"""
    logging.basicConfig(level=logging.DEBUG)

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.apiKey = ''  # 用户名
        self.secretKey = ''  # 密码
        self.host = ''  # 服务器地址
        self.per = 0
        self.cur = 0
        self.max = 0
        self.min = 7000

        self.currency = 'cny'  # 货币类型（usd或者cny）

        self.ws = None  # websocket应用对象
        self.thread = None  # 工作线程

    #######################
    ## 通用函数
    #######################

    # ----------------------------------------------------------------------
    def readData(self, evt):
        """解压缩推送收到的数据"""
        # 创建解压器
        decompress = zlib.decompressobj(-zlib.MAX_WBITS)

        # 将原始数据解压成字符串
        inflated = decompress.decompress(evt) + decompress.flush()

        # 通过json解析字符串
        data = json.loads(inflated)

        return data

    # ----------------------------------------------------------------------
    def generateSign(self, params):
        """生成签名"""
        l = []
        for key in sorted(params.keys()):
            l.append('%s=%s' % (key, params[key]))
        l.append('secret_key=%s' % self.secretKey)
        sign = '&'.join(l)
        return hashlib.md5(sign.encode('utf-8')).hexdigest().upper()

    # ----------------------------------------------------------------------
    def onMessage(self, ws, evt):
        """信息推送"""
        # print 'onMessage'
        data = self.readData(evt)
        # print data
        if 'data' in str(data[0]):
            self.per = self.cur
            self.cur = float(data[0]['data']['last'])

            if self.cur > self.per:
                if self.cur > self.max:
                    self.max = self.cur

                if self.per != 0 and self.per < self.min:
                    self.min = self.per
                print 'U'
            else:
                if self.cur < self.min:
                    self.min = self.cur
                print 'D'

            print 'max', self.max
            print 'min', self.min
            print data[0]['data']['last']

    # ----------------------------------------------------------------------
    def onError(self, ws, evt):
        """错误推送"""
        print 'onError'
        print evt

    # ----------------------------------------------------------------------
    def onClose(self, ws):
        """接口断开"""
        print 'onClose'

    # ----------------------------------------------------------------------
    def onOpen(self, ws):
        """接口打开"""
        print 'onOpen'
        try:
            ws.send("{'event':'addChannel','channel':'ok_sub_spotcny_btc_ticker','binary':'true'}")
        except:
            print 'EEEEEEEEEEEEEEEEEE'

    # ----------------------------------------------------------------------
    def connect(self, host, apiKey, secretKey, trace=False):
        """连接服务器"""
        self.host = host
        self.apiKey = apiKey
        self.secretKey = secretKey

        # if self.host == OKCOIN_CNY:
        #     self.currency = CURRENCY_CNY
        # else:
        #     self.currency = CURRENCY_USD

        websocket.enableTrace(trace)

        self.ws = websocket.WebSocketApp(host,
                                         on_message=self.onMessage,
                                         on_error=self.onError,
                                         on_close=self.onClose,
                                         on_open=self.onOpen)

        self.thread = Thread(target=self.ws.run_forever)
        self.thread.start()


if __name__ == '__main__':
    api = OkCoinApi()
    api.connect('wss://real.okcoin.cn:10440/websocket/okcoinapi', '', '')
