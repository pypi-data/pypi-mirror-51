from lmf.dbv2 import db_command ,db_query
from lmf.bigdata import pg2csv
import sys 
import os 
import time 
from zlhawq.dst.core import add_quyu_tmp,restart_quyu_tmp
import traceback


def add_quyu_kunming(quyu):
    conp=['gpadmin','since2015','192.168.169.90:5433','base_db','public']

    add_quyu_tmp(quyu,conp)



def restart_quyu_kunming(quyu):
    conp=['gpadmin','since2015','192.168.169.90:5433','base_db','public']

    restart_quyu_tmp(quyu,conp)


def add_quyu(quyu,loc='aliyun'):
    if loc=='kunming':
        add_quyu_kunming(quyu)



def restart_quyu(quyu,loc='aliyun'):
    if loc=='kunming':
        restart_quyu_kunming(quyu)