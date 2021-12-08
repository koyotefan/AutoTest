# encoding=utf-8

import os
import sys
import traceback
import requests
import json
from collections import OrderedDict


from src.common.PrivateLog import Log

class SnrAgentClient(object):
    def __init__(self, _L):
        self.L = _L

    def request(self, _url, _req_data):

        response = requests.post(_url, json=_req_data)

        #print '-- SnrAgentClient.request'
        #print _req_data

        self.L.info('[{:10}] RESULT - {}'.format('STEP', response.status_code))

        if response.status_code != 200:
            return (False, response.json())

        # _req_data 와 response 에 대한 판단을 여기서 합니다.
        resp_data = response.text

        if self.diff_expect_and_response(json.loads(_req_data, object_pairs_hook=OrderedDict),
                                         json.loads(resp_data, object_pairs_hook=OrderedDict)):
            return (True, resp_data)
        else:
            return (False, resp_data)


    def diff_expect_and_response(self, _req_dict, _resp_dict):
        if "EXPECT" not in _req_dict.keys():
            return True

        for k in _req_dict["EXPECT"]:
            if k[2:] not in _resp_dict.keys():
                return False

            if _req_dict["EXPECT"][k] != _resp_dict[k[2:]]:
                return False

        return True

if __name__ == '__main__':

    l = Log('DEG', 'TestSnrAgentClient.log', True)
    client = SnrAgentClient(l.get())

    od = OrderedDict([(u'PRIMITIVE', u'LOG-MONITOR-START'), (u'TARGET', [u'CDS', u'SDM'])])
    (result, text) = client.request('http://127.0.0.1:9091', od)

    print result
    print text