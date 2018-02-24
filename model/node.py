#coding: utf-8

from settings import DATABASES
from .mysql_server import MysqlServer

class NodeInfo(object):
    @staticmethod
    def node_info():
        db = MysqlServer(DATABASES)
        sql = "select * from node"
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def group_list():
        db = MysqlServer(DATABASES)
        sql = "select distinct `node_group` from node"
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def node_list(node_group):
        db = MysqlServer(DATABASES)
        sql = "select `node_ip` from node where node_group=" + '"' + node_group + '"'
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def get_node_port(node_ip):
        db = MysqlServer(DATABASES)
        sql = "select `port` from node where node_ip='%s'" % node_ip
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def insert_con_usage(con_id, con_ip, node_ip):
        db = MysqlServer(DATABASES)
        sql = "insert into con_usage(con_id, con_ip, node_ip) values('%s','%s','%s')" % (con_id, con_ip, node_ip)
        db.execute_sql(sql)
        db.close()
        return 0

    @staticmethod
    def delete_con_usage(con_id):
        db = MysqlServer(DATABASES)
        sql = "delete from con_usage where con_id='%s'" % con_id
        db.execute_sql(sql)
        db.close()
        return 0

    @staticmethod
    def con_usage_info():
        db = MysqlServer(DATABASES)
        sql = "select `con_id`,`con_ip`,`node_ip`,`user_name`,`con_app`,`con_desc` from con_usage"
        result = db.run_sql(sql)
        db.close()
        return result

    @staticmethod
    def get_con_usage_modify(result):
        db = MysqlServer(DATABASES)
        sql = "select `con_id`,`con_ip`,`node_ip`,`user_name`,`con_app`,`con_desc` from con_usage where con_id='%s'" % result
        ret = db.run_sql(sql)
        db.close()
        return ret


