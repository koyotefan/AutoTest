# encoding=utf-8

import os
import sys
import traceback

from src.common.PrivateLog import Log
from src.common.Misc import read_json_file
from src.common.Misc import get_snr_dir

class SnrFileReader(object):
    def __init__(self, _L):
        self.L = _L
        self.snr_base_dir = get_snr_dir()

        self.d = {}

    def set_base_dir(self, _dir):
        self.snr_base_dir = _dir

    def read(self, _filename):
        self.d = {}
        self.d = read_json_file(self.snr_base_dir, _filename)

        #print '--- SnrFileReader.read'
        #print self.d

    def count(self):
        return len(self.d)

    def get(self, _index):
        if not self.d:
            return {}

        key = _index if type(_index) is str else str(_index) if type(_index) is int else ''
        v = {}

        try:
            v = self.d[key]
        except KeyError:
            pass

        return v

if __name__ == '__main__':

    l = Log('DEB', 'TestSnrFileReader.log', True)
    r = SnrFileReader(l.get())

    r.set_base_dir('/PG/AUTOV/SnrExecutor/SnrList')

    r.read('가입자_신규_A1.snr')
    for i in range(r.count()):
        print i
        print r.get(str(i))

