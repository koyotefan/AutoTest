
# encoding=utf-8

import os
import sys
import pyodbc
import traceback
import time

class PDB(object):
    def __init__(self):
        self.cnxn = None
        self.cursor = None

    '''
    def init(self, _dsn):
        if not self.connect(_dsn):
            time.sleep(0.5)
            return self.connect(_dsn)

        return (True, '')
    '''

    def init(self, _dsn):
        try:
            self.connect(_dsn)
        except:
            time.sleep(0.5)
            return self.connect(_dsn)
        return True

    def connect(self, _dsn):
        self.cnxn = pyodbc.connect(dsn=_dsn)
        return True

    '''
    def connect(self, _dsn):
        try:
            self.cnxn = pyodbc.connect(dsn=_dsn)
        except:
            _, exc_value, exc_traceback = sys.exc_info()
            return (False, traceback.format_exception(exc_value,
                                                      exc_value,
                                                      exc_traceback))

        return (True, '')

    def connect(self, _dict):
        # self.cnxn = pyodbc.connect(dsn=_dsn)
        self.cnxn = pyodbc.connect(driver={_dict["DRIVER"]},
                                   server='{}:{}'.format(_dict["HOST"][0], _dict["HOST"][1]),
                                   database=_dict["DATABASE"],
                                   uid=_dict["ID"],
                                   pwd=_dict["PW"])


        return True
    '''


    def close(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None

        if self.cnxn:
            self.cnxn.close()
            self.cnxn = None


    def execute(self, _sql, _commit=True):
        if not self.cnxn:
            return False

        if not self.cursor:
            self.cursor = self.cnxn.cursor()

        self.cursor.execute(_sql)

        if _commit:
            self.cnxn.commit()

        return True

    def query(self, _sql):
        if not self.cnxn:
            return ([], 'db conntction lost')

        if not self.cursor:
            self.cursor = self.cnxn.cursor()

        self.cursor.execute(_sql)
        fetch_list = self.cursor.fetchall()

        # dict 을 반환할꺼예요.
        ret_dict = {}
        index = 0
        for col in [d[0] for d in self.cursor.description]:
            ret_dict[col] = str(fetch_list[0][index])
            index += 1

        return ret_dict

    def commit(self):
        self.cnxn.commit()

    # def TestGetColumnNames(self):
    def test_get_column_names(self):
        sql = '''SELECT * FROM T_SUBSCRIBER_INFO limit 1'''

        cur = self.cnxn.cursor()
        cur.execute(sql)
        column_names = [d[0] for d in cur.description]

        print column_names

if __name__ == '__main__':

    db = PDB()

    if db.init('LOCAL_SUBS'):
        rows = db.query('SELECT * FROM T_SUBSCRIBER_INFO limit 1')
        for row in rows:
            print row

    db.close()


