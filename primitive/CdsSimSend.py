# encoding=utf-8

import json
from src.common.TargetAgent import TargetAgent
from collections import OrderedDict

'''
{
    "PARAMETER": {
        "job_code": {
            "value": "C1",
            "length": 2,
            "allow": ["ALL"]
        },
        "mdn": {
            "value": "01011118888",
            "length": 12,
            "allow": ["ALL"]
        },
        "new_mdn": {
            "value": "01012349999",
            "length": 12,
            "allow": ["D3"]
        },
        "min": {
            "value": "1011118888",
            "length": 10,
            "allow": ["A1", "D3", "G1", "C1", "I2", "I3"]
        },
        "new_min": {
            "value": "1012349999",
            "length": 10,
            "allow": ["D3", "C1"]
        },
        "product_id": {
            "value": "NA00005325",
            "length": 10,
            "allow": ["A1", "D3", "Z1", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "G1", "C1", "I2", "I3", "H1", "H2", "I4", "I5", "I6", "I7", "I8", "I9", "IA", "IB", "IC", "ID", "IE", "IF", "IG", "IH", "II", "IJ", "IK", "IL", "IM", "IN", "IO", "IP", "IQ", "IR", "IS", "IT", "IU", "IX", "IY", "IZ", "QK", "QL", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "RA", "RB", "RC", "RD", "RE", "RF", "RG", "RH", "RI", "RJ", "RK", "RL", "RM", "RN", "RO", "RT", "RU", "RV", "RW", "S1", "S2", "S3", "S4", "T1", "T2", "T3", "J1", "J2", "J3", "J4", "J5", "J6", "J7", "J8", "Q8", "Q9", "H3", "H4", "H5", "H6", "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9", "LA", "LB", "LC", "LD", "LE", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9", "YA", "YB", "YC", "YD", "YE", "YF", "QC", "QD", "QE", "QF", "QG", "QH", "QI", "QJ", "H7", "H8", "H9", "HA", "HB", "HC", "HD", "HE", "HF", "HG", "HH", "HI", "HJ", "HK", "HL", "HM", "HN", "HO", "HP", "HQ", "HR", "N1", "N2", "W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"]
        },
        "service_id": {
            "value": "",
            "length": 10,
            "allow": ["A1", "D3", "G1", "C1"]
        },
        "network": {
            "value": "0001",
            "length": 8,
            "allow": ["A1", "D3", "Z1", "G1", "C1"]
        },
        "block_data_roaming_id": {
            "value": "0",
            "length": 1,
            "allow": ["I2", "I3"]
        },
        "block_data_roaming_provider_id": {
            "value": "1",
            "length": 1,
            "allow": ["I2", "I3"]
        },
        "allow_mvoip_yn": {
            "value": "1",
            "length": 1,
            "allow": ["I4", "I5", "IY", "IZ", "QK", "QL"]
        },
        "tablet_yn": {
            "value": "0",
            "length": 1,
            "allow": ["A1", "D3", "Z1", "G1", "C1"]
        },
        "os_ver": {
            "value": "01",
            "length": 2,
            "allow": ["A1", "D3", "Z1", "G1", "C1"]
        },
        "device_model": {
            "value": "SSTE",
            "length": 4,
            "allow": ["A1", "D3", "Z1", "G1", "C1"]
        },
        "block_harmful_yn": {
            "value": "1",
            "length": 1,
            "allow": ["I2", "I3"]
        },
        "block_roaming_data_yn": {
            "value": "1",
            "length": 1,
            "allow": ["L1", "L2"]
        },
        "block_roaming_mvoip_yn": {
            "value": "1",
            "length": 1,
            "allow": ["L3", "L4"]
        },
        "zone_code": {
            "value": "0002",
            "length": 4,
            "allow": ["Y5", "Y6", "Y7", "Y8", "Y9"]
        },
        "ca": {
            "value": "3",
            "length": 1,
            "allow": ["A1", "D3", "Z1", "G1", "C1"]
        },
        "aprf": {
            "value": "0",
            "length": 1,
            "allow": ["A1", "D3", "Z1", "G1", "C1"]
        },
        "imsi": {
            "value": "450051011118888",
            "length": 15,
            "allow": ["A1", "D3", "G1", "C1"]
        },
        "mvno_campany": {
            "value": "0",
            "length": 1,
            "allow": ["A1", "D3", "Z1", "G1", "C1"]
        },
        "limit_subs": {
            "value": "0",
            "length": 1,
            "allow": ["ALL"]
        },
        "roaming_qos_param": {
            "value": "3",
            "length": 1,
            "allow": ["L5", "L7", "L9", "LB", "LD"]
        },
        "coupon_end_time": {
            "value": "201609051927",
            "length": 12,
            "allow": ["Y9"]
        },
        "coupon_type": {
            "value": "03",
            "length": 2,
            "allow": ["Y9"]
        },
        "coupon_pin": {
            "value": "91348599978",
            "length": 11,
            "allow": ["Y9"]
        },
        "reserved": {
            "value": "01234567891",
            "length": 11,
            "allow": ["ALL"]
        }
    },
    "EXPECT": {
        "r$RESULT": "OK"
    }
}
'''

class  CdsSimSend(TargetAgent):
    '''
    CDS-SIM-SEND primitive 에 대한 구현체 입니다.
    CDS Simulator 의 설정 Config 가 변경되면, CDS_SIM.conf 변경및 해당 프리미티브 변경도 고려해야 합니다.
    '''
    def __init__(self):
        TargetAgent.__init__(self)

        self.param_dict = None
        self.exp_dict = {}

    def __str__(self):
        return 'CdsSimSend'

    def make_request_data(self, _constant):
        self.param_dict = _constant.get_template("CDS_SIM.conf")
        l_dict = _constant.get_var()
        TargetAgent.set(self, l_dict["TARGET_AGENT"])

        for key in l_dict:
            if key.startswith('r$'):
                self.exp_dict[key] = l_dict[key]
            else:
                self._reflect_to_dict(self.param_dict, l_dict)

        return self._verify(l_dict, _constant)

    # SnrConstant 의 reflect_to_dict() 을 참고하여, ["value"] 에 맞춰서 변형
    def _reflect_to_dict(self, _obj_dict, _ref_dict):

        for key in _obj_dict.keys():
            if key in _ref_dict.keys():
                _obj_dict[key]["value"] = _ref_dict[key]

            if (isinstance(_obj_dict[key]["value"], str) or isinstance(_obj_dict[key]["value"], unicode)) and \
                _obj_dict[key]["value"].startswith("$"):
                if _obj_dict[key]["value"][1:] in _ref_dict.keys():
                    _obj_dict[key]["value"] = _ref_dict[_obj_dict[key]["value"][1:]]


    def _verify(self, _l_dict, _constant):

        if not self.param_dict:
            return False

        for val in self.param_dict.values():
            if val["value"].startswith('$'):
                return False

        return True

    def request(self):
        ret_dict = {}

        ret_dict["PARAMETER"] = self.param_dict
        ret_dict["EXPECT"] = self.exp_dict

        return json.dumps(ret_dict, sort_keys=False)

    def uri(self):
        return TargetAgent.uri(self, self.__class__.__name__)

    def do(self, _req_dict):
        '''
        SnrAgent 에서는 /SmSimSet 에서 데이터를 받으면, do() 를 호출 합니다.
        '''
        import os
        import time
        from src.common.Misc import get_sim_info, read_json_file

        res_dict = {}
        res_dict["RESULT"] = "OK"

        info_dict = get_sim_info("cds_sim")

        # result 파일을 reset 해요.
        ret_file = os.path.join(info_dict["dir"], info_dict["ret"])

        try:
            os.remove(ret_file)
        except OSError:
            pass

        # config 파일 변경을 하고 있어요.
        conf_file = os.path.join(info_dict["dir"], info_dict["conf"])
        with open(conf_file, "w") as f :
            try:
                f.write(json.dumps(_req_dict["PARAMETER"], sort_keys=False, indent=4))
            except IOError:
                res_dict["RESULT"] = "NOK"
                res_dict["REASON"] = "can't write data conf {}".format(conf_file)


        # result 파일에 데이터를 그대로 읽어서, 결과로 전달해요.
        for _ in range(30):
            try:
                os.path.getsize(ret_file)
            except OSError:
                time.sleep(0.1)
                continue

            return read_json_file(info_dict["dir"], info_dict["ret"])

        res_dict["RESULT"] = "NOK"
        res_dict["REASON"] = "can't read result data {}".format(ret_file)
        return res_dict
