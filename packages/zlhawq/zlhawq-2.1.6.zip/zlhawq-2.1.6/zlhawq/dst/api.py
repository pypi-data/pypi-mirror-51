from lmf.dbv2 import db_command ,db_query
from lmf.bigdata import pg2csv
import sys 
import os 
import time 
from zlhawq.dst.core import add_quyu_tmp,restart_quyu_tmp
import traceback


def add_quyu(quyu):
    conp=['gpadmin','since2015','192.168.4.179','base_db','dst']

    add_quyu_tmp(quyu,conp)



def restart_quyu(quyu):
    conp=['gpadmin','since2015','192.168.4.179','base_db','dst']

    restart_quyu_tmp(quyu,conp)