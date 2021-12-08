# encoding=utf-8

import sys
import traceback
import json
from src.common.TargetAgent import TargetAgent

'''
  {
    "TARGET_DB": {
        #"HOST": ["192.168.10.45", "20303"],
        #"DATABASE": "pcrf",
        #"DRIVER": "/altibase/altibase_home/lib/libaltibase_odbc-64bit-ul32.so",
        #"ID": "pcrf",
        #"PW": "pcrf1234"
        "DSN_NAME" : "PDB_SUBS_P"
    },
    "PARAMETER": {
        "SQL": "select TERMINAL_MODEL_CODE from T_SUBSCRIBER_INFO WHERE MDN='01012349876'"
    },
    "EXPECT": {
        "r$TERMINAL_MODEL_CODE": "2222",
        "r$RESULT": "OK"
    }
 }

'''

class  DBSubsSelect(TargetAgent):
    '''
    DB-가입자-확인 primitive 에 대한 구현체 입니다.
    '''
    def __init__(self):
        TargetAgent.__init__(self)

        self.db_dict = None
        self.param_dict = {}
        self.exp_dict = {}

    def __str__(self):
        return 'DBSubsSelect'

    def make_request_data(self, _constant):
        l_dict = _constant.get_var()
        TargetAgent.set(self, l_dict["TARGET_AGENT"])
        self.param_dict["SQL"] = l_dict["SQL"]

        for key in l_dict:
            if key.startswith('r$'):
                self.exp_dict[key] = l_dict[key]
            #elif key == "TARGET_AGENT":
            #    TargetAgent.set(self, l_dict[key])
            elif key == 'TARGET_DB':
                self.db_dict = _constant.get_targetdb(l_dict[key])
            elif key == 'SQL':
                self.param_dict[key] = _constant.reflect_to_str(self.param_dict[key], l_dict)
            else:
                pass

        return self._verify(_constant)

    def _verify(self, _constant):

        if self.db_dict == None:
            self.db_dict = _constant.get_targetdb("$PDB_SUBS_P")

        for val in self.db_dict.values():
            if isinstance(val, str) and '$' in val:
                return False

        if not self.param_dict:
            return False

        for val in self.param_dict.values():
            if val.startswith('$'):
                return False

        for val in self.exp_dict.values():
            if val.startswith('$'):
                return False

        return True

    def request(self):
        ret_dict = {}

        ret_dict["TARGET_DB"] = self.db_dict
        ret_dict["PARAMETER"] = self.param_dict
        ret_dict["EXPECT"] = self.exp_dict

        return json.dumps(ret_dict, sort_keys=False)

    def uri(self):
        return TargetAgent.uri(self, self.__class__.__name__)

    def do(self, _req_dict):

        res_dict = {}
        res_dict["RESULT"] = "OK"

        # 파라메터와 TARGET_DB 를 찾아야 합니다.
        if ("TARGET_DB" or "PARAMETER") not in _req_dict.keys():
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "Missing TARGET_DB or PARAMETER tag"
            return res_dict

        from src.common.DB import PDB
        db = PDB()

        try:
            db.init(_req_dict["TARGET_DB"]["DSN_NAME"])
        except:
            _, exc_value, exc_traceback = sys.exc_info()
            print traceback.format_exception(exc_value,
                                             exc_value,
                                             exc_traceback)

            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "DB Connection Error"
            return res_dict

        # DB 조회
        sql = _req_dict["PARAMETER"]["SQL"]

        try:

            val_dict = db.query(sql)
            for key in val_dict:
                res_dict[key] = val_dict[key]

        except:
            _, exc_value, exc_traceback = sys.exc_info()
            print traceback.format_exception(exc_value,
                                             exc_value,
                                             exc_traceback)

            db.close()
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "DB Select Fail"

            return res_dict

        db.close()
        return res_dict