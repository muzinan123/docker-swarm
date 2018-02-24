#coding:utf-8

""" 执行mysql语句 """
import hashlib

from settings import DATABASES
from .mysql_server import MysqlServer

class UserSqlOperation(object):
    @staticmethod
    def check_adm_login(admname):
        db = MysqlServer(DATABASES)
        sql = "select `name`,`password`,`user_group` from user where name='%s'" % admname
        ret = db.run_sql(sql)
        db.close()
        return ret