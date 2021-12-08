# encoding=utf-8

import json
from src.common.TargetAgent import TargetAgent

'''
{
    "CMD": "netstat -na | grep 10200 | grep LISTEN | wc -l",
    "EXPECT": {
        "r$RET": "0",
        "r$RESULT": "OK"
    }
}
'''

class ShellCmd(TargetAgent):
    '''
    SHELL-CMD primitive 에 대한 구현체 입니다.
    '''

    def __init__(self):
        TargetAgent.__init__(self)

        self.cmd = ''
        self.exp_dict = {}

    def __str__(self):
        return 'ShellCmd'


    def make_request_data(self, _constant):
        l_dict = _constant.get_var()
        TargetAgent.set(self, l_dict["TARGET_AGENT"])

        for key in l_dict:
            if key.startswith('r$'):
                self.exp_dict[key] = l_dict[key]
            elif key == 'CMD':
                if not isinstance(l_dict[key], str) and not isinstance(l_dict[key], unicode):
                    self.cmd = ''
                else:
                    self.cmd = _constant.reflect_to_str(l_dict[key], l_dict)
            else:
                pass

        return self._verify(_constant)

    def _verify(self, _constant):
        if not self.cmd:
            return False

        return True


    def request(self):
        ret_dict = {}

        ret_dict["CMD"] = self.cmd
        ret_dict["EXPECT"] = self.exp_dict

        return json.dumps(ret_dict, sort_keys=False)


    def uri(self):
        return TargetAgent.uri(self, self.__class__.__name__)


    def do(self, _req_dict):

        res_dict = {}
        res_dict["RESULT"] = "OK"

        if "CMD" not in _req_dict.keys() :
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "Missing CMD tag"
            return res_dict

        if not _req_dict["CMD"]:
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "Nothing CMD"
            return res_dict

        # 프로세스 RUN
        import subprocess

        ret = subprocess.check_output(_req_dict["CMD"], shell=True)
        res_dict["RET"] = ret.strip()
        return res_dict