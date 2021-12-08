# encoding=utf-8

import json
from src.common.TargetAgent import TargetAgent

'''
{
    "FILES": ["/data/PG/LOG/RT/SESSION.MMSC*.01.20161118"],
    "WORD": ["Error", "Kill", "Down", "error", "Warning", "ERR"],
    "EXPECT": {
        "r$CNT": "0"
    }
}
'''

class LogMonitorCheck(TargetAgent):
    '''
    LOG-MONITOR-CHECK primitive 에 대한 구현체 입니다.
    '''

    def __init__(self):
        TargetAgent.__init__(self)

        self.task_id = ''
        self.file_list = []
        self.word_list = []
        self.exp_dict = {}


    def __str__(self):
        return 'LogMonitorCheck'


    def make_request_data(self, _constant):
        l_dict = _constant.get_var()
        TargetAgent.set(self, l_dict["TARGET_AGENT"])
        self.task_id = l_dict["TASK_ID"]

        for key in l_dict:
            if key.startswith('r$'):
                self.exp_dict[key] = l_dict[key]
            #elif key == "TARGET_AGENT":
            #    TargetAgent.set(self, l_dict[key])
            elif key == 'TARGET':
            #    TargetAgent.set(self, l_dict["TARGET_AGENT"])
                self.file_list = TargetAgent.get_log_file_list(self, l_dict[key])
                self.file_list = self._reflect_to_list(self.file_list, l_dict)

            elif key == 'WORD':
                self.word_list = l_dict[key]
            else:
                pass

        return self._verify(_constant)

    def _reflect_to_list(self, _obj_list, _l_dict):
        return [stmt.replace("$YYYYMMDD", _l_dict["YYYYMMDD"]) for stmt in _obj_list]

    def _verify(self, _constant):
        if not self.file_list:
            return False

        if not self.word_list:
            return False

        return True


    def request(self):
        ret_dict = {}

        ret_dict["TASK_ID"] = self.task_id
        ret_dict["FILES"] = self.file_list
        ret_dict["WORD"] = self.word_list
        ret_dict["EXPECT"] = self.exp_dict

        return json.dumps(ret_dict, sort_keys=False)


    def uri(self):
        return TargetAgent.uri(self, self.__class__.__name__)


    def do(self, _req_dict):
        '''
        파일에 쓰여진 값을 읽고, Check 를 한 뒤에 업데이트 한다.
        '''

        res_dict = {}
        res_dict["RESULT"] = "OK"
        res_dict["CNT"] = "0"
        res_dict["DETAILS"] = {}
        # res_dict["DETAILS"] = { "FILE" : "TEXT", "FILE" : "TEXT", ... }

        # 파일을 읽고, word 와 맞춘후에 판별을 합니다.
        # 주어진 로그를 저달하는 것도 일이죠.
        # 한번 체크한 노마는 dict 에서 날립니다.

        import os
        from src.common.Misc import read_json_file, get_logset_file_name

        fname = get_logset_file_name()

        logset_dict = {}
        try:
            logset_dict = read_json_file(fname[:fname.rfind(os.sep)],
                                         fname[fname.rfind(os.sep)+1:])
        except IOError:
            pass

        # 본인의 Task ID 를 찾습니다.
        task_id = _req_dict["TASK_ID"]
        sub_logset_dict = {}
        if task_id in logset_dict.keys():
            sub_logset_dict = logset_dict[task_id]

        sum = 0
        except_cnt = 0
        for target in _req_dict["FILES"]:
            try:
                cnt, text = self._cnt_and_text_include_word(target,
                                                      self._get_offset(target, sub_logset_dict),
                                                      _req_dict["WORD"])
                sum += cnt
                res_dict["DETAILS"][target] = text
            except IOError:
                except_cnt += 1

        if except_cnt == len(_req_dict["FILES"]):
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "can't read log files"
            return res_dict

        res_dict["CNT"] = str(sum)
        return res_dict


    def _get_offset(self, _target, _logset_dict):
        # logset 에 있으면 거기서 부터, 없으면 0 부터..
        if _target in _logset_dict.keys():
            return _logset_dict[_target]
        else:
            return 0


    def _cnt_and_text_include_word(self, _target, _offset_long, _word_list):
        # Log 파일을 열어서 실제
        text_list = []
        with open(_target, 'r') as fd:
            fd.seek(_offset_long)
            while True:
                line = fd.readline()

                if not line:
                    break

                text_list.append(line)

        text = '\n'.join(text_list)
        ret_cnt = 0
        for word in _word_list:
            if word in text:
                ret_cnt += 1
                continue

        return (ret_cnt, text)
