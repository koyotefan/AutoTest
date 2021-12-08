# encoding=utf-8

import os
import time

from src.common.Misc import get_history_dir, get_date, get_time, print_add_result

OKGREEN = '\033[92m'
NOKRED = '\033[91m'
COMPBLUE = '\033[94m'
ENDC = '\033[0m'

class HistoryWriter(object):
    def __init__(self):
        self.dir = ''

        self.ok = "{}[OK]{}".format(OKGREEN, ENDC)
        self.nok = "{}[NOK]{}".format(NOKRED, ENDC)

        self.group_name = ''
        self.tot_snr_cnt = 0
        self.succ_snr_cnt = 0
        self.fail_snr_cnt = 0

        self.fname_stack = []
        self.fname_detail_stack = []

        self.display_depth = 0

    def start(self):
        '전체 검증을 실행할 때, 호출됩니다.'
        'n 개의 그룹을 실행할 수 있습니다.'

        self.dir = os.path.join(get_history_dir(), get_date() + '_' + get_time())

        # dir 를 생성합니다.
        # dir 내의 detail 디렉토리를 생성합니다.
        try:
            os.mkdir(self.dir, 0755)
            os.mkdir(os.path.join(self.dir, 'detail'), 0755)
        except OSError:
            return False

        return True

    def stop(self):
        '전체 검증을 끝낼 때, 호출됩니다.'
        '결과를 적어야 겠지요'
        pass

    def start_group(self, _group_name, _tot_snr_cnt):
        self.group_name = _group_name
        self.tot_snr_cnt = _tot_snr_cnt
        self.succ_snr_cnt = 0
        self.fail_snr_cnt = 0

        self.fname_stack.append(os.path.join(self.dir, _group_name))

    def end_group(self):

        txt = "{} - TOTAL :{:03d} SUCCESS : {:03d} FAIL : {:03d}".format(self.group_name,
                                                                        self.tot_snr_cnt,
                                                                        self.succ_snr_cnt,
                                                                        self.fail_snr_cnt)

        with open(self.fname_stack[-1], "a") as open_fd:
            open_fd.write("\n")
            open_fd.write("{}{}{}\n".format(COMPBLUE, txt, ENDC))

        self.fname_stack.pop(-1)

    def start_snr(self, _snr_name, _snr_task_id, _snr_depth):
        '1개의 시나리오가 시작될 때, 호출됩니다.'
        self.display_depth = (_snr_depth-1) * 4
        self.display_depth = 0 if self.display_depth < 0 else self.display_depth

        self.fname_detail_stack.append(os.path.join(self.dir, 'detail', _snr_task_id))
        txt = "{}{: >{prec}}- {}".format(time.strftime("%Y-%m-%d %H:%M:%S"),
                                        ' ',
                                        _snr_task_id,
                                        prec=self.display_depth)

        with open(self.fname_stack[-1], "a") as open_fd:
            open_fd.write("{}\n".format(txt))


    def end_snr(self, _snr_name, _result_f, _snr_depth):
        '1개의 시나리오가 종료될 때, 호출됩니다.'
        self.display_depth = (_snr_depth-1) * 4
        self.display_depth = 0 if self.display_depth < 0 else self.display_depth

        self.fname_detail_stack.pop(-1)

        result_str = self.ok if _result_f else self.nok
        txt = "{}{: >{prec}}SCENARIO - {}".format(time.strftime("%Y-%m-%d %H:%M:%S"),
                                                ' ',
                                                _snr_name,
                                                prec=self.display_depth)

        with open(self.fname_stack[-1], "a") as open_fd:
            open_fd.write("{}\n".format(print_add_result(txt, result_str)))

        if _result_f:
            self.succ_snr_cnt += 1
        else:
            self.fail_snr_cnt += 1

    def detail(self, _title, _data):
        '동작에 대한 상세정보를 기록할 때, 호출됩니다.'
        txt = "{}    {}\n{}".format(time.strftime("%Y-%m-%d %H:%M:%S"), _title, _data)

        with open(self.fname_detail_stack[-1], "a") as open_fd:
            open_fd.write("{}\n".format(txt))


    def end_step(self, _title, _result_f):
        '1개의 step 이 종료도리 때, 호출됩니다.'
        result_str = self.ok if _result_f else self.nok
        txt = "{}{: >{prec}}    STEP - {}".format(time.strftime("%Y-%m-%d %H:%M:%S"),
                                                    ' ',
                                                    _title,
                                                    prec=self.display_depth)

        with open(self.fname_stack[-1], "a") as open_fd:
            open_fd.write("{}\n".format(print_add_result(txt, result_str)))

