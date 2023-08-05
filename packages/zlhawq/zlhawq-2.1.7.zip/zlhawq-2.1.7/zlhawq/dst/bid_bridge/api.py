from lmf.dbv2 import db_command ,db_query
from lmf.bigdata import pg2csv
import sys 
import os 
from fabric import Connection
from zlhawq.dst.bid_bridge.core import add_quyu_tmp,restart_quyu_tmp
import traceback

def add_quyu(quyu,tag='all'):
    if quyu.startswith('anhui_anqing'):
        add_quyu_tmp(quyu)
    elif quyu.startswith('zlsys'):
        add_quyu_tmp(quyu)
    else:
        print("暂不支持 区域%s"%quyu)


def restart_quyu(quyu,tag='all'):
    if quyu.startswith('anhui_anqing'):
        restart_quyu_tmp(quyu)
    elif quyu.startswith('zlsys'):
        restart_quyu_tmp(quyu)
    else:
        print("暂不支持 区域%s"%quyu)
