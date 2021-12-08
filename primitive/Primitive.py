# encoding=utf-8

MODULE_MATRIX = {
    'SM-SIM-SET' : 'src.primitive.SmSimSet',
    'SM-SIM-START' : 'src.primitive.SmSimStart',
    'SM-SIM-STOP' : 'src.primitive.SmSimStop',
    'PROCESS-STOP' : 'src.primitive.ProcessStop',
    'PROCESS-START' : 'src.primitive.ProcessStart',
    'PROCESS-RESTART' : 'src.primitive.ProcessRestart',
    'PROCESS-INIT' : 'src.primitive.ProcessInit',
    'PROCESS-KILL' : 'src.primitive.ProcessKill',
    'LOG-MONITOR-START' : 'src.primitive.LogMonitorStart',
    'LOG-MONITOR-CHECK' : 'src.primitive.LogMonitorCheck',
    'DB-가입자-생성' : 'src.primitive.DBSubsCreate',
    'DB-가입자-삭제' : 'src.primitive.DBSubsDelete',
    'DB-가입자-확인' : 'src.primitive.DBSubsSelect',
    'DB-PGW-세션-생성' : 'src.primitive.DBPgwSessionCreate',
    'DB-DPI-세션-생성' : 'src.primitive.DBDpiSessionCreate',
    'DB-PGW-세션-삭제' : 'src.primitive.DBPgwSessionDelete',
    'DB-DPI-세션-삭제' : 'src.primitive.DBDpiSessionDelete',
    'DB-QUERY-실행' : 'src.primitive.DBExecute',
    'CDS-SIM-SEND' : 'src.primitive.CdsSimSend',
    'CDS-SIM-START' : 'src.primitive.CdsSimStart',
    'CDS-SIM-STOP' : 'src.primitive.CdsSimStop',
    'MMSC-SIM-SEND' : 'src.primitive.MmscSimSend',
    'MMSC-SIM-START' : 'src.primitive.MmscSimStart',
    'MMSC-SIM-STOP' : 'src.primitive.MmscSimStop',
    'SLEEP' : 'src.primitive.Sleep',
    'SHELL-CMD' : 'src.primitive.ShellCmd'
}

class Primitive(object):
    '''
    Primitive 를 생성하는 객체 입니다.
    '''
    def __init__(self, _name):
        self.name = str(_name)
        self.inst = None

    def make_request_data(self, _constant):
        try:
            self.inst = self._create(self.name)
        except:
            return False

        return self.inst.make_request_data(_constant)

    def _create(self, _name):
        components = MODULE_MATRIX[_name].split('.')

        mod = __import__(MODULE_MATRIX[_name], fromlist=components[-1])
        obj = getattr(mod, components[-1])()

        # print obj
        return obj

    def request(self):
        return self.inst.request()

    def uri(self):
        return self.inst.uri()

    def do(self):
        return self.inst.do()


if __name__ == '__main__':

    import sys
    from src.common.PrivateLog import Log
    from src.executor.SnrConstant import SnrConstant

    log_inst = Log('DEB', 'TempPrimitive.log', True)
    log = log_inst.get()

    c = SnrConstant(log)

    c.push_var()

    '''
    # DB-가입자-생성 테스트
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "DB-가입자-생성",
        "MDN" : "01028071121",
        "r$RESULT" : "OK"
        })

    p = Primitive("DB-가입자-생성")
    '''

    '''
    # DB-가입자-확인
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "DB-가입자-확인",
        "SQL" : "select TERMINAL_MODEL_CODE from T_SUBSCRIBER_INFO WHERE MDN = $MDN",
        "r$RESULT" : "OK",
        "r$TERMINAL_MODEL_CODE" : "$NEW_TERMINAL_MODEL_CODE"
        })

    p = Primitive("DB-가입자-확인")
    '''

    '''
    # SLEEP
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "DB-가입자-확인",
        "SQL" : "select TERMINAL_MODEL_CODE from T_SUBSCRIBER_INFO WHERE MDN=$MDN",
        "r$RESULT" : "OK",
        "r$TERMINAL_MODEL_CODE" : "$NEW_TERMINAL_MODEL_CODE"
        })

    p = Primitive("SLEEP")
    p.make_request_data(c)
    p.do()
    '''

    '''
    # SM-SIM-SET
    c.set_primitive_var({
        "PRIMITIVE" : "SM-SIM-SET",
        "SET" : [
            {
                "MDN" : "01099991111",
                "TIMESTAMP" : "20151231001525",
                "PGW_IP" : "$PGW_GROUP_3G",
                "NETWORK_TOPOLOGY" : "W",
                "3GPP_SGSN_MCC_MNC" : "45005"

            },
            {
                "TIMESTAMP" : "$YYYYMMDDhhmmss",
                "PGW_IP" : "$PGW_GROUP_3G",
                "NETWORK_TOPOLOGY" : "W",
            }
        ],
        "r$RESULT" : "OK"
    })

    p = Primitive("SM-SIM-SET")
    '''

    '''
    # LOG-MONITOR-CHECK
    c.set_primitive_var({
        "PRIMITIVE" : "LOG-MONITOR-CHECK",
        "TARGET" : ["MMSC"],
        "WORD" : ["Error", "Kill", "Down", "error", "Warning", "ERR"],
        "r$CNT" : "0"
        }
    )

    p = Primitive("LOG-MONITOR-CHECK")
    '''

    '''
    # LOG-MONITOR-START
    c.set_primitive_var({
        "PRIMITIVE" : "LOG-MONITOR-START",
        "TARGET" : ["CDS", "P_SDM"],
        "r$RESULT" : "OK"
        })

    p = Primitive("LOG-MONITOR-START")
    '''

    '''
    # MMSC-SEND
    c.set_primitive_var({
        "PRIMITIVE" : "MMSC-SIM-SEND",
        #"PARAMETER" : {},
        "r$RESULT" : "OK",
        "r$MDN" : "$MDN"
        })

    p = Primitive("MMSC-SIM-SEND")
    '''

    '''
    # DB-PGW-세션-생성
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "MDN" : "01099998888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "DB-PGW-세션-생성",
        "r$RESULT" : "OK"
        })

    p = Primitive("DB-PGW-세션-생성")
    '''

    '''
    # DB-DPI-세션-생성
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "TARGET_DB" : "$PDB_SESSION_S",
        "SLEEP_TIME" : "0.5",
        "MDN" : "01099998888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "DB-DPI-세션-생성",
        "r$RESULT" : "OK"
        })

    p = Primitive("DB-DPI-세션-생성")
    '''

    '''
    # CDS-SIM-SEND
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "job_code" : "C1",
        "mdn" : "01011118888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "CDS-SIM-SEND",
        "PARAMETER" : {},
        "r$RESULT" : "OK"
        })

    p = Primitive("CDS-SIM-SEND")
    '''

    '''
    #  PROCESS-STOP
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "job_code" : "C1",
        "mdn" : "01011118888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "PROCESS-STOP",
        "TARGET" : ["LISTENER201"],
        "r$RESULT" : "OK",
        "r$CNT" : "0"
        })

    p = Primitive("PROCESS-NORMAL-STOP")
    '''

    '''
    #  PROCESS-START
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "job_code" : "C1",
        "mdn" : "01011118888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "PROCESS-START",
        "TARGET" : ["LISTENER201"],
        "r$RESULT" : "OK",
        "r$CNT" : "1"
        })

    p = Primitive("PROCESS-START")
    '''

    '''
    #  PROCESS-RESTART
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "job_code" : "C1",
        "mdn" : "01011118888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "PROCESS-RESTART",
        "TARGET" : ["LISTENER201"],
        "r$RESULT" : "OK",
        "r$CNT" : "1"
        })

    p = Primitive("PROCESS-RESTART")
    '''

    '''
    #  SHELL-CMD
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "job_code" : "C1",
        "mdn" : "01011118888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "SHELL-CMD",
        "CMD" : "netstat -na | grep $MMSC_PORT | grep LISTEN | wc -l",
        "r$RESULT" : "OK",
        "r$CNT" : "0"
        })

    p = Primitive("SHELL-CMD")
    '''

    '''
    #  MMSC-SIM-START
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "job_code" : "C1",
        "mdn" : "01011118888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "MMSC-SIM-START",
        "r$RESULT" : "OK"
        })

    p = Primitive("MMSC-SIM-START")
    '''

    '''
    #  MMSC-SIM-STOP
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "job_code" : "C1",
        "mdn" : "01011118888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "MMSC-SIM-STOP",
        "r$RESULT" : "OK"
        })

    p = Primitive("MMSC-SIM-STOP")
    '''

    '''
    #  DB-QUERY-실행
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "job_code" : "C1",
        "mdn" : "01011118888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "DB-QUERY-실행",
        "SQL" : [
            "delete from T_PGW_GROUP_INFO WHERE CLIENT_IP = '$PGW_GROUP_SA'",
            "delete from T_PGW_GROUP_INFO WHERE CLIENT_IP = '$PGW_GROUP_SB'",
            "delete from T_PGW_GROUP_INFO WHERE CLIENT_IP = '$PGW_GROUP_SC'",
            "delete from T_PGW_GROUP_INFO WHERE CLIENT_IP = '$PGW_GROUP_DA'",
            "delete from T_PGW_GROUP_INFO WHERE CLIENT_IP = '$PGW_GROUP_DB'",
            "delete from T_PGW_GROUP_INFO WHERE CLIENT_IP = '$PGW_GROUP_DC'"
            ],
        "r$RESULT" : "OK"
        })

    p = Primitive("DB-QUERY-실행")
    '''

    '''
    #  PROCESS-INIT
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "job_code" : "C1",
        "mdn" : "01011118888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "PROCESS-INIT",
        "TARGET" : ["MMSC201"],
        "r$RESULT" : "OK"
        })

    p = Primitive("PROCESS-INIT")
    '''

    '''
    #  SM-SIM-START
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "job_code" : "C1",
        "mdn" : "01011118888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "SM-SIM-START",
        "r$RESULT" : "OK"
        })

    p = Primitive("SM-SIM-START")
    '''

    '''
    #  SM-SIM-STOP
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "job_code" : "C1",
        "mdn" : "01011118888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "SM-SIM-STOP",
        "r$RESULT" : "OK"
        })

    p = Primitive("SM-SIM-STOP")
    '''

    '''
    #  CDS-SIM-START
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "job_code" : "C1",
        "mdn" : "01011118888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "CDS-SIM-START",
        "r$RESULT" : "OK"
        })

    p = Primitive("CDS-SIM-START")
    '''

    '''
    #  CDS-SIM-STOP
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "job_code" : "C1",
        "mdn" : "01011118888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "CDS-SIM-STOP",
        "r$RESULT" : "OK"
        })

    p = Primitive("CDS-SIM-STOP")
    '''

    '''
    #  PROCESS-KILL
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "job_code" : "C1",
        "mdn" : "01011118888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "PROCES-KILL",
        "TARGET" : ["MMSC203"],
        "r$RESULT" : "OK"
        })

    p = Primitive("PROCESS-KILL")
    '''

    #  CDS-SIM-SEND
    c.set_var({
        "PRIMITIVE" : "LOCAL-VAR-SET",
        "SLEEP_TIME" : "0.5",
        "JOB_CODE" : "H1",
        "MDN" : "01011118888",
        "TERMINAL_MODEL_CODE" : "1111",
        "NEW_TERMINAL_MODEL_CODE" : "2222"
        })

    c.set_primitive_var({
        "PRIMITIVE" : "CDS-SIM-SEND",
        "JOB_CODE" : "$JOB_CODE",
        "PRODUCT_ID" : "ABCDE",
        "MDN" : "$MDN",
        "r$RESULT" : "OK"
        })

    p = Primitive("CDS-SIM-SEND")

    if not p.make_request_data(c):
        print '*********** Fail'
        sys.exit()

    #print p.request()
    #print p.uri()
    log.info(p.request())
    log.info(p.uri())

