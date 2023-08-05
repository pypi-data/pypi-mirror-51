from lmf.dbv2 import db_command ,db_query
from lmf.bigdata import pg2csv
import sys 
import os 
from fabric import Connection
from zlhawq.dst.bid.core import add_quyu_tmp_pc,restart_quyu_tmp_pc,add_quyu_zlsys,restart_quyu_zlsys
import traceback


def add_quyu(quyu,tag='all'):
    if quyu.startswith('anhui_anqing'):
        add_quyu_tmp_pc(quyu,tag)
    elif quyu.startswith('zlsys'):
        add_quyu_zlsys(quyu)
    else:
        print("暂不支持 区域%s"%quyu)


def restart_quyu(quyu):
    if quyu.startswith('anhui_anqing'):
        restart_quyu_tmp_pc(quyu,tag)
    elif quyu.startswith('zlsys'):
        restart_quyu_zlsys(quyu)
    else:
        print("暂不支持 区域%s"%quyu)


