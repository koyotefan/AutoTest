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
        "DSN_NAME" : "PDB_SESSION_P_45",
        "TABLE_INDEX" : "04"
    },
    "PARAMETER": {
        "MDN": "01028071121"
    },
    "EXPECT": {
        "r$RESULT": "OK"
    }
}
'''

class  DBPgwSessionDelete(TargetAgent):
    '''
    DB-PGW-세션-삭제 primitive 에 대한 구현체 입니다.
    '''
    def __init__(self):
        TargetAgent.__init__(self)

        self.db_dict = None
        self.param_dict = None
        self.exp_dict = {}

    def __str__(self):
        return 'DBPgwSessionDelete'

    def make_request_data(self, _constant):
        l_dict = _constant.get_var()
        TargetAgent.set(self, l_dict["TARGET_AGENT"])

        self.param_dict = {"MIN" : l_dict["MIN"]}

        for key in l_dict:
            if key.startswith('r$'):
                self.exp_dict[key] = l_dict[key]
            elif key == 'TARGET_DB':
                self.db_dict = _constant.get_targetdb(l_dict[key], l_dict["MIN"])
            else:
                _constant.reflect_to_dict(self.param_dict, l_dict)

        return self._verify(_constant, l_dict["MIN"])

    def _verify(self, _constant, _min):

        if self.db_dict == None:
            self.db_dict = _constant.get_targetdb("$PDB_SESSION_P", _min)

        for val in self.db_dict.values():
            if isinstance(val, str) and val.startswith('$'):
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

        # DB 삭제
        sql = self._delete_sql(_req_dict["PARAMETER"], _req_dict["TARGET_DB"])
        try:
            db.execute(sql)
        except:
            _, exc_value, exc_traceback = sys.exc_info()
            print traceback.format_exception(exc_value,
                                             exc_value,
                                             exc_traceback)

            db.close()
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "DB Delete Fail"

            return res_dict

        db.close()
        return res_dict

    def _delete_sql(self, _param_dict, _db_dict):
        return "DELETE FROM T_SESSION_INFO_{} WHERE MIN='{}'".format(_db_dict["TABLE_INDEX"], _param_dict["MIN"])