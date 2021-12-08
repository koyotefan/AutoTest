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

class MmscSimStop(TargetAgent):
    '''
    MMSC-SIM-STOP primitive 에 대한 구현체 입니다.
    '''

    def __init__(self):
        TargetAgent.__init__(self)

        self.exp_dict = {}

    def __str__(self):
        return 'MmscSimStop'


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


    def do(self):
        pass