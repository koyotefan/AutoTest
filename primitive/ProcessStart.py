# encoding=utf-8

import json
from src.common.TargetAgent import TargetAgent

'''
{
    "PROCESS": ["LISTENER201"],
    "EXPECT": {
        "r$CNT": "1",
        "r$RESULT": "OK"
    }
}
'''

class ProcessStart(TargetAgent):
    '''
    PROCESS-START primitive 에 대한 구현체 입니다.
    '''

    def __init__(self):
        TargetAgent.__init__(self)

        self.proc_list = []
        self.exp_dict = {}

    def __str__(self):
        return 'ProcessStart'


    def make_request_data(self, _constant):
        l_dict = _constant.get_var()
        TargetAgent.set(self, l_dict["TARGET_AGENT"])

        for key in l_dict:
            if key.startswith('r$'):
                self.exp_dict[key] = l_dict[key]
            elif key == 'TARGET':
                if not isinstance(l_dict[key], list):
                    self.proc_list = []
                else:
                    self.proc_list = l_dict[key]
            else:
                pass

        return self._verify(_constant)

    def _verify(self, _constant):
        if not self.proc_list:
            return False

        return True


    def request(self):
        ret_dict = {}

        ret_dict["PROCESS"] = self.proc_list
        ret_dict["EXPECT"] = self.exp_dict

        return json.dumps(ret_dict, sort_keys=False)


    def uri(self):
        return TargetAgent.uri(self, self.__class__.__name__)

    def do(self, _req_dict):

        res_dict = {}
        res_dict["RESULT"] = "OK"

        if "PROCESS" not in _req_dict.keys() :
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "Missing PROCESS tag"
            return res_dict

        if not _req_dict["PROCESS"]:
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "Nothing process name"
            return res_dict

        # 프로세스 RUN
        import subprocess

        cnt = 0
        for pname in _req_dict["PROCESS"]:
            ret = subprocess.check_output('startMP -p {}'.format(pname), shell=True)
            ret = subprocess.check_output('disMP | grep {}'.format(pname), shell=True)

            if 'Active' in ret:
                cnt += 1

        res_dict["CNT"] = str(cnt)
        return res_dict