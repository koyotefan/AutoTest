# encoding=utf-8

import json
import copy
from src.common.TargetAgent import TargetAgent

'''
{
    "PARAMETER": [{
        "TIMESTAMP": "20151231001525",
        "PGW_IP": "172.1.1.1",
        "MDN": "01012349876",
        "MIN": "1012349876",
        "IMSI": "450051012349876",
        "MSISDN": "821012349876",
        "ACCOUNT_SESSION_ID": "123456789ABCDEFGH",
        "LOCATION_ID": "1234ABCD1234ABCD",
        "NETWORK_TOPOLOGY": "W",
        "3GPP_SGSN_MCC_MNC": "45005"
    }, {
        "TIMESTAMP": "20161122151952",
        "PGW_IP": "172.1.1.1",
        "MDN": "01012349876",
        "MIN": "1012349876",
        "IMSI": "450051012349876",
        "MSISDN": "821012349876",
        "ACCOUNT_SESSION_ID": "123456789ABCDEFGH",
        "LOCATION_ID": "1234ABCD1234ABCD",
        "NETWORK_TOPOLOGY": "W",
        "3GPP_SGSN_MCC_MNC": "45005"
    }],
    "EXPECT": {
        "r$RESULT": "OK"
    }
}
'''

class  SmSimSet(TargetAgent):
    '''
    SM-SIM-SET primitive 에 대한 구현체 입니다.
    '''
    def __init__(self):
        TargetAgent.__init__(self)

        self.param_list = None
        self.exp_dict = {}

    def __str__(self):
        return 'SmSimSet'

    def make_request_data(self, _constant):
        template_dict = _constant.get_template("SM_SIM.conf")
        l_dict = _constant.get_var()
        TargetAgent.set(self, l_dict["TARGET_AGENT"])

        for key in l_dict:
            if key.startswith('r$'):
                self.exp_dict[key] = l_dict[key]
            # elif key == "TARGET_AGENT":
            #    TargetAgent.set(self, l_dict[key])
            elif key == "SET":
                self.param_list = self._make_param_list(template_dict, l_dict["SET"])

                '''
                for SM 으로 보낼 dict in 파라메터 LIST:
                    SM 으로 보낼 dict 에 l_dict 을 적용해요.
                    적용하다가, Value 에 $ 가 있다면, l_dict 을 다시 적용해요.
                '''

                for nest_dict in self.param_list:
                    _constant.reflect_to_dict(nest_dict, l_dict)

            else:
                pass

        return self._verify(_constant)

    def _make_param_list(self, _template_dict, _set_list):
        ret_list = []

        for nest_dict in _set_list:
            # 여기서는, 그냥 Template 을 이용하여 오꾸만 만들어서 return 합시다.
            new_dict = copy.deepcopy(_template_dict)

            for key in nest_dict.keys():
                new_dict[key] = nest_dict[key]

            ret_list.append(new_dict)

        return ret_list

    def _verify(self, _constant):

        # param_list 가 없을 수도 있어요..
        # SM 에서 NOT FOUND 를 주면 되니까요.

        for item_dict in self.param_list:
            for val in item_dict.values():
                if val.startswith('$'):
                    return False

        for val in self.exp_dict.values():
            if val.startswith('$'):
                return False

        return True

    def request(self):
        ret_dict = {}

        ret_dict["PARAMETER"] = self.param_list
        ret_dict["EXPECT"] = self.exp_dict

        return json.dumps(ret_dict, sort_keys=False)

    def uri(self):
        return TargetAgent.uri(self, self.__class__.__name__)

    def do(self, _req_dict):
        '''
        SnrAgent 에서는 /SmSimSet 에서 데이터를 받으면, do() 를 호출 합니다.
        '''
        import os
        from src.common.Misc import get_sim_info

        res_dict = {}
        res_dict["RESULT"] = "OK"

        info_dict = get_sim_info("sm_sim")
        conf_fname = os.path.join(info_dict["dir"], info_dict["conf"])

        with open(conf_fname, "w") as f :
            try:
                f.write(json.dumps(_req_dict["PARAMETER"], sort_keys=False, indent=4))
            except:
                res_dict["RESULT"] = "NOK"
                res_dict["REASON"] = "can't read data conf {}".format(conf_fname)

        return res_dict

