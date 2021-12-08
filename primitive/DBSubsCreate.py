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
        "MDN": "01028071121",
        "MIN": "1028071121",
        "MSISDN": "821028071121",
        "NETWORK_ID": "0001",
        "PRODUCT_ID": " ",
        "SERVICE_ID": " ",
        "IN_TYPE": " ",
        "IN_TIME": " ",
        "PRODUCT_TYPE": "1",
        "DATA_USAGE_LEVEL": "0",
        "MVOIP_APPLY_FG": "N",
        "MVOIP_LIMIT_OVER_FG": "N",
        "TABLET_PC_YN": "N",
        "OS_VERSION": "01",
        "TERMINAL_MODEL_CODE": "1111",
        "YOUNG_HARM_INFO_BLOCK": "N",
        "W_DATA_ROAMING_BLOCK": "N",
        "L_DATA_ROAMING_BLOCK": "N",
        "W_ROAMING_MVOIP_BLOCK": "N",
        "L_ROAMING_MVOIP_BLOCK": "N",
        "BLACK_LIST_FG": "N",
        "DESCRIPTION": "AUTOV",
        "R1": "",
        "R2": "",
        "R3": "1",
        "R4": "1",
        "CA": "0",
        "APRF": "N",
        "BTV": "0",
        "TSPORTS": "0",
        "TLOL": "0",
        "TCLOUD_GAME": "0",
        "W_QOS1_ROAMING_LIMIT_OVE": "N",
        "W_QOS2_ROAMING_LIMIT_OVE": "N",
        "L_QOS1_ROAMING_LIMIT_OVE": "N",
        "L_QOS2_ROAMING_LIMIT_OVE": "N",
        "TIME_SVC_A": "N",
        "TIME_SVC_B": "N",
        "TIME_SVC_C": "N",
        "TIME_SVC_D": "N",
        "TIME_SVC_E": "N",
        "ZONE_SVC_A": "N",
        "ZONE_SVC_B": "N",
        "ZONE_SVC_C": "N",
        "ZONE_SVC_D": "N",
        "ZONE_SVC_E": "N",
        "ZONE_SVC_F": "N",
        "ZONE_SVC_G": "N",
        "ZONE_SVC_H": "N",
        "ZONE_SVC_I": "N",
        "ZONE_SVC_J": "N",
        "IMS_EMR": "N",
        "DOMESTIC_TETH_BLOCK": "N",
        "ROAMING_TETH_BLOCK": "N",
        "MVNO_COMPANY": "0",
        "LIMIT_SUBS_FG": "0",
        "ZONE_ID": "",
        "R5": "",
        "R6": "",
        "R7": "",
        "R8": "",
        "R9": "",
        "R10": "",
        "ROAMING_PRODUCT": "N",
        "SPON": "0",
        "BUGS_FREE": "0",
        "ARMY_ACTION": "0",
        "R11": "0",
        "R12": "0",
        "R13": "0",
        "R14": "0",
        "R15": "0",
        "R16": "0",
        "R17": "0",
        "R18": "0",
        "R19": "0",
        "R20": "0",
        "R21": "0",
        "R22": "0",
        "R23": "0",
        "R24": "0",
        "R25": "0",
        "R26": "0",
        "R27": "0",
        "R28": "0",
        "R29": "0",
        "R30": "0"
    },
    "EXPECT": {
        "r$RESULT": "OK"
    }
}
'''

class  DBSubsCreate(TargetAgent):
    '''
    DB-가입자-생성 primitive 에 대한 구현체 입니다.
    가입자 테이블이 변경되면, DB_가입자_테이블.conf 변경이 필요 합니다.
    '''
    def __init__(self):
        TargetAgent.__init__(self)

        self.db_dict = None
        self.param_dict = None
        self.exp_dict = {}

    def __str__(self):
        return 'DBSubsCreate'

    def make_request_data(self, _constant):
        # conf 에서 T_SUBSCRIBER_INFO 의 Column 및 default 값을 config 에서 읽어 옵니다.
        # 읽은 값에 대고, _constant 가 그동안 축적한 값을 반영시킵니다.
        self.param_dict = _constant.get_template("DB_가입자_테이블.conf")
        l_dict = _constant.get_var()
        TargetAgent.set(self, l_dict["TARGET_AGENT"])

        for key in l_dict:
            if key.startswith('r$'):
                self.exp_dict[key] = l_dict[key]
        #    elif key == "TARGET_AGENT":
        #        TargetAgent.set(self, l_dict[key])
            elif key == 'TARGET_DB':
                self.db_dict = _constant.get_targetdb(l_dict[key])
            else:
                _constant.reflect_to_dict(self.param_dict, l_dict)

        return self._verify(_constant)

    def _verify(self, _constant):

        if self.db_dict == None:
            self.db_dict = _constant.get_targetdb("$PDB_SUBS_P")

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
        sql = self._delete_sql(_req_dict["PARAMETER"])

        try:
            db.execute(sql)
        except:
            pass

        # DB 생성
        sql = self._insert_sql(_req_dict["PARAMETER"])

        try:
            db.execute(sql)
        except:
            _, exc_value, exc_traceback = sys.exc_info()
            print traceback.format_exception(exc_value,
                                             exc_value,
                                             exc_traceback)

            db.close()
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "DB Insert Fail"

            return res_dict

        db.close()
        return res_dict

    def _insert_sql(self, _dict):
        sql_list = []

        sql_list.append('INSERT INTO T_SUBSCRIBER_INFO (')
        for param in _dict.keys():
            sql_list.append(param)
            sql_list.append(",")

        # 마지막 , 를 날리고요.
        sql_list[-1] = ") VALUES ("
        for param in _dict.keys():
            if param == 'IN_TIME':
                sql_list.append("SYSDATE")
            elif param == 'NETWORK_ID':
                sql_list.append("{}".format(_dict[param]))
            elif param == 'IN_TYPE':
                sql_list.append("0")
            else:
                sql_list.append("'{}'".format(_dict[param]))
            sql_list.append(",")

        # 마지막 , 를 날리고요.
        sql_list[-1] = ")"

        return ''.join(sql_list)

    def _delete_sql(self, _dict):
        return "DELETE FROM T_SUBSCRIBER_INFO WHERE MDN='{}'".format(_dict["MDN"])