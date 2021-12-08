# encoding=utf-8

import os
import sys

from socket import *
import select

import time
import copy

class HistoryBroker(object):
    def __init__(self):
        self.conn_list = []
        self.sub_conn_list = []

    def run(self, port=10198):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind(('', port))
        sock.listen(5)
        self.conn_list.append(sock)

        while self.conn_list:
            in_list, out_list, err_list = select.select(self.conn_list, [], [], 10)

            if not in_list:
                continue

            for conn in in_list:
                if conn == sock:
                    new_conn, addr_info = sock.accept()

                    if self._new_conn_process(new_conn):
                        self.conn_list.append(new_conn)
                    else:
                        new_conn.close()
                else:
                    data = ''
                    try:
                        data = conn.recv()
                    except :
                        self.conn_list.remove(conn)
                        conn.close()
                        continue

                    if not data:
                        self.conn_list.remove(conn)
                        conn.close()
                    else:
                        self.broadcast(data)


    def broadcast(self, _data):
        temp_list = copy.copy(self.sub_conn_list)

        for sub_conn in temp_list:
            try:
                sub_conn.sendall(_data)
            except:
                self.sub_conn_list.append(sub_conn)

    def _new_conn_process(self, _new_conn):
        '''
        처음 연결이 될 때, 자신이 PUB 를 할 것인지, SUB 를 할 것인지를 등록할 것 입니다.
        '''
        attr = _new_conn.recv(3)

        if not attr:
            return False

        if attr == 'PUB':
            return True
        elif attr == 'SUB':
            self.sub_conn_list.append(_new_conn)
            return True
        else:
            return False


if __name__ == '__main__':

    hb = HistoryBroker()
    hb.run(port=10198)
