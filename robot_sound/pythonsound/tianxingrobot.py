# -*- coding:utf-8 -*-
from urllib.request import urlopen, Request
from urllib.error import URLError
import json
from urllib.parse import urlencode


# 图灵机器人接口参数
class TuringChatMode(object):
    def __init__(self):
        # API接口地址
        self.turing_url = 'http://api.tianapi.com/txapi/tuling/index?'

    def get_turing_text(self, text):
        turing_url_data = dict(
            key='xxxxxxxxxxx',
            question=text,
        )
        self.request = Request(self.turing_url + urlencode(turing_url_data))
        try:
            w_data = urlopen(self.request)
        except URLError:
            raise IndexError("No internet connection available to transfer txt data")
            # 如果发生网络错误，断言提示没有可用的网络连接来传输文本信息
        except:
            raise KeyError("Server wouldn't respond (invalid key or quota has been maxed out)")
            # 其他情况断言提示服务相应次数已经达到上限

        response_text = w_data.read().decode('utf-8')
        json_result = json.loads(response_text)
        return json_result['newslist']


turing = TuringChatMode()
reply = turing.get_turing_text("你好")
print(reply)  # 输出完整json
print(reply[0]['reply'])  # 提取出回复文字
