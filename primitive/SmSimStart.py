# encoding=utf-8

import json
from src.common.TargetAgent import TargetAgent

'''
 {
    "EXPECT": {
        "r$RESULT": "OK"
    }
 }
'''

class SmSimStart(TargetAgent):
    '''
    SM-SIM-START primitive 에 대한 구현체 입니다.
    '''

    def __init__(self):
        TargetAgent.__init__(self)

        self.exp_dict = {}

    def __str__(self):
        return 'SmSimStart'


    def make_request_data(self, _constant):
        l_dict = _constant.get_var()
        TargetAgent.set(self, l_dict["TARGET_AGENT"])

        for key in l_dict:
            if key.startswith('r$'):
                self.exp_dict[key] = l_dict[key]
            else:
                pass

        return self._verify(_constant)

    def _verify(self, _constant):
        return True


    def request(self):
        ret_dict = {}
        ret_dict["EXPECT"] = self.exp_dict

        return json.dumps(ret_dict, sort_keys=False)


    def uri(self):
        return TargetAgent.uri(self, self.__class__.__name__)


    def do(self, _req_dict):
        '''
        SnrAgent 에서는 /SmSimStart 에서 데이터를 받으면, do() 를 호출합니다.
        '''

        res_dict = {}
        res_dict["RESULT"] = "OK"

        from src.agent.ChildProcess import ChildProcess
        from src.common.Misc import get_sim_info

        child = ChildProcess()
        if not child.init(get_sim_info("sm_sim")):
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "Unkown simualtor info for sm_sim"
            return res_dict


        if not child.run():
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "simualtor run fail"
            return res_dict

        return res_dict

