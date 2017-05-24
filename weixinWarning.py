# encoding: UTF-8

import requests
import json

import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def get_token():
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    values = {'corpid': 'wxb8617a1c5d4896b0',
              'corpsecret': 'dbCXU5xcB8Bx3-yAXiXIZz3KiB5P87o2gq7hB_H74gXxevjljuoWSYpF7URE2F3q',
              }
    req = requests.post(url, params=values)
    data = json.loads(req.text)
    return data["access_token"]


def send_msg(agentid, message, totag=1):
    # print "send_msg"
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + get_token()
    values = """{"touser" : "" ,
      "toparty":"",
      "totag":"%s",
      "msgtype":"text",
      "agentid":"%s",
      "text":{
        "content": "%s"
      },
      "safe":"0"
      }""" % (str(totag), str(agentid), str(message).encode('utf-8'))

    # data = json.loads(values)
    requests.post(url, values)


if __name__ == '__main__':
    # print get_token()
    send_msg('0', '''test''')
