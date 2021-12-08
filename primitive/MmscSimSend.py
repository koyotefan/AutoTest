# encoding=utf-8

import json
import copy
from src.common.TargetAgent import TargetAgent

'''
{
    "PARAMETER": {
        "TIMESTAMP": "20161118203931",
        "DEVICE_IP": "2001:0d88:1111:1010::/64",
        "IP_VERSION": "6",
        "NETWORK": "2",
        "PGW_GROUP_ID": "SA"
    },
    "EXPECT": {
        "r$MDN": "01012349876",
        "r$RESULT": "OK"
    }
}
'''

class  MmscSimSend(TargetAgent):
    '''
    MMSC-SIM-SEND primitive 에 대한 구현체 입니다.
    '''
    def __init__(self):
        TargetAgent.__init__(self)

        self.param_dict = None
        self.exp_dict = {}

    def __str__(self):
        return 'MmscSimSend'

    def make_request_data(self, _constant):
        self.param_dict = _constant.get_template("MMSC_SIM.conf")
        l_dict = _constant.get_var()

        _constant.reflect_to_dict(self.param_dict, l_dict)

        for key in l_dict:
            if key.startswith('r$'):
                self.exp_dict[key] = l_dict[key]
            elif key == "TARGET_AGENT":
                TargetAgent.set(self, l_dict[key])
            #elif key == 'PARAMETER':
            #    _constant.reflect_to_dict(self.param_dict, l_dict)
            else:
                pass

        return self._verify(l_dict, _constant)


    def _verify(self, _l_dict, _constant):

        if not self.param_dict:
            return False

        # make_request_data() 에서 'PARAMETER' 만나지 않을 수도 있어서,
        # 아래 내용이 추가 되었습니다.
        for val in self.param_dict.values():
            if val.startswith('$'):
                _constant.reflect_to_dict(self.param_dict, _l_dict)

        for val in self.param_dict.values():
            if val.startswith('$'):
                return False

        return True

    def request(self):
        ret_dict = {}

        ret_dict["PARAMETER"] = self.param_dict
        ret_dict["EXPECT"] = self.exp_dict

        return json.dumps(ret_dict, sort_keys=False)

    def uri(self):
        return TargetAgent.uri(self, self.__class__.__name__)

    def do(self):
        pass
