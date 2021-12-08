# encoding=utf-8

import json
from src.common.TargetAgent import TargetAgent

'''
{
    "PROCESS": ["MMSC201"],
    "EXPECT": {
        "r$RESULT": "OK"
    }
}
'''

class ProcessInit(TargetAgent):
    '''
    PROCESS-START primitive 에 대한 구현체 입니다.
    '''

    def __init__(self):
        TargetAgent.__init__(self)

        self.proc_list = []
        self.exp_dict = {}

        self.pkg_id = ''
        self.process_seq = '1'
        self.cmd_code = '9001'
        self.argv1 = '0'



    def __str__(self):
        return 'ProcessInit'


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

        self.pkg_id = self._get_pkg_id()
        if not self.pkg_id:
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "can't get package id"
            return res_dict


        # 프로세스 RUN
        import subprocess

        cnt = 0
        for pname in _req_dict["PROCESS"]:

            ret = subprocess.check_output('disMP | grep {}'.format(pname), shell=True)
            if not ret:
                continue

            ret_list = ret.split()
            if len(ret_list) != 10:
                continue

            cmd = self._make_init_cmd(ret_list[2], ret_list[4])

            ret = subprocess.check_output('{}'.format(cmd), shell=True)
            ret = subprocess.check_output('disMP | grep {}'.format(pname), shell=True)

            if 'Active' in ret:
                cnt += 1

        res_dict["CNT"] = str(cnt)
        return res_dict


    def _get_pkg_id(self):
        import os
        import ConfigParser

        home = os.environ['PFM_HOME']

        if not home:
            return ''

        config = ConfigParser.ConfigParser()

        try:
            config.read(os.path.join(home, 'CFG/PFM.MAIN.CFG'))
        except IOError:
            return ''

        pkg_id = config.get('COMMON', 'DEFAULT_SYSTEM_ID').strip()
        return pkg_id

    def _make_init_cmd(self, _service_id, _process_id):
        return 'pfmCMD {} {} {} {} {} {}'.format(self.pkg_id,
                                                _service_id,
                                                _process_id,
                                                self.process_seq,
                                                self.cmd_code,
                                                self.argv1)