#coding: utf-8

import tornado.web
import threading
import sys
import json
import uuid
import time

from .base import BaseHandler
from myswarm import Myswarm
from settings import template_variables



sys.path.append("..")
from model.data_manage import DataManage
from model.node import NodeInfo
from config import basejson

class Main(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('node/main.html',)

class NodeManage(BaseHandler):
    @tornado.web.authenticated
    def get(self,*args, **kwargs):
        threads = []
        node_update = threading.Thread(target=self._update_node)
        threads.append(node_update)
        node_pass = threading.Thread(target=self._get_pass)
        threads.append(node_pass)
        for t in threads:
            t.setDaemon(True)
            t.start()
        node_data = NodeInfo.node_info()
        node_data_handled = DataManage.manage_node_info(node_data)
        self.render("node/node_manage.html", node_data = node_data_handled)

    def _update_node(self):
        node_data = NodeInfo.node_info()
        myswarm = Myswarm()
        for line in node_data:
            node_ip = line[2]
            node_port = line[3]
            if myswarm.ping_port(node_ip, node_port) == 1:
                continue
            else:
                node_info = myswarm.node_list(node_ip, node_port)
                NodeInfo.node_info_update(node_info, node_ip)

    def _get_pass(self):
        pass

class Top(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("base.html", name = template_variables)

class LeftGroup(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('node/leftgroup.html')

class GroupList(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", None)
        lv = self.get_argument("lv", None)
        name = self.get_argument("n", None)
        alldata = []
        if id == None and lv == None and name == None:
            alldata = self._getgroup()
        elif id != "" and lv == "0":
            alldata = self._getnode(id, name)
        elif lv == "1":
            alldata = self._getcontainer(id, name)
        self.write(json.dumps(alldata))

    def _getgroup(self):
        group_data = []
        group_ret  = NodeInfo.group_list()
        for i in DataManage.group_list(group_ret):
            group_data.append(i)
        return group_data


    def _getnode(self, id, name):
        node_ret  = NodeInfo.node_list(name)
        node_data = DataManage.node_list(node_ret, id, name)
        return node_data

    def _getcontainer(self, id, name):
        container_ret  = NodeInfo.container_list(name)
        container_data = DataManage.container_list(container_ret, id, name)
        return container_data

class RightNode(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        node_ip = self.get_argument('node_ip', None)
        print(node_ip)
        if node_ip is None:
            self.write("Something Wrong")
            return
        else:
            node_port = NodeInfo.get_node_port(node_ip)[0][0]
            myswarm = Myswarm()
            con_data = myswarm.container_list(node_ip, node_port)
            self.render('node/rightnode.html', con_data = con_data, node_ip = node_ip)

class ConCreate(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        node_ip = self.get_argument('node_ip', None)
        if node_ip is None:
            self.write("Something Wrong")
            return
        else:
            node_port = NodeInfo.get_node_port(node_ip)[0][0]
            myswarm = Myswarm()
            images_data = myswarm.images_list(node_ip, node_port)
            self.render('node/con_create.html', node_ip = node_ip, images = images_data)

    def post(self, *args, **kwargs):
        json_ret = json.loads(basejson[0])
        node_ip = self.get_argument('node_ip', 'None')
        if node_ip == 'None':
            print("There is no node ip")
            return
        port_ret = NodeInfo.get_node_port(node_ip)
        if len(port_ret) < 1:
            print("There is no port of the node")
            return
        else:
            node_port = port_ret[0][0]

        con_dict = {}
        for key in ['Cmd', 'Image', 'CpuPeriod', 'CpuQuota', 'CpuShares', 'Memory']:
            con_dict[key] = self.get_argument(key.lower())
            if key == 'Cmd' and con_dict[key] != "":
                json_ret[key] = con_dict[key].split()
            elif key == 'Image' and con_dict[key] != "":
                json_ret[key] = con_dict[key]
            elif con_dict[key] != "":
                json_ret['HostConfig'][key] = int(con_dict[key])

        myswarm = Myswarm()
        json_ret['Name'] = str(uuid.uuid4())[0:13]
        json_ret['Hostname'] = json_ret['Name']

        container_id = myswarm.create_container(node_ip, node_port, json_ret)
        if not container_id:
            print("Can not create the Container")
            return
        ret = myswarm.start_container(node_ip, node_port, container_id)

class ConAction(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        node_ip = self.get_argument('node_ip')
        con_id  = self.get_argument('con_id')

        port_ret = NodeInfo.get_node_port(node_ip)
        if len(port_ret) < 1:
            print("There is no port of the node")
            return
        else:
            node_port = port_ret[0][0]

        myswarm = Myswarm()
        con_data_handled = myswarm.container_info(node_ip, node_port, con_id)
        self.render("node/con_action.html", name=template_variables, node_ip=node_ip,
            node_port=node_port, con_id=con_id, con_data=con_data_handled)

class ConStart(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kargs):
        con_dict = {}
        for key in ['node_ip', 'port', 'con_id']:
            con_dict[key] = self.get_argument(key)

        myswarm = Myswarm()
        if not con_dict['con_id']:
            self.write("There is no container id")
        print("      Starting the container......")
        ret = myswarm.start_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])


class ConStop(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kargs):
        con_dict = {}
        for key in ['node_ip', 'port', 'con_id']:
            con_dict[key] = self.get_argument(key)
        myswarm = Myswarm()
        myswarm.stop_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])


class ConRestart(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kargs):
        con_dict = {}
        for key in ['node_ip', 'port', 'con_id']:
            con_dict[key] = self.get_argument(key)

        container_ip = {}
        myswarm = Myswarm()
        if not con_dict['con_id']:
            self.write("There is no container id")
        myswarm.stop_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])
        time.sleep(2)
        myswarm.start_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])


class ConDestroy(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kargs):
        con_dict = {}
        for key in ['node_ip', 'port', 'con_id']:
            con_dict[key] = self.get_argument(key)
        myswarm = Myswarm()
        myswarm.destroy_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])

class ConManage(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        con_id = self.get_argument('con_id', 'none')
        if con_id == 'none':
            con_data = NodeInfo.con_usage_info()
        else:
            con_data = NodeInfo.get_con_usage_modify(con_id)
        con_data_handled = DataManage.manage_con_usage_info(con_data)
        self.render("node/con_list.html", name=template_variables, con_data=con_data_handled)

class ConModify(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        con_id = self.get_argument('con_id')
        con_data = NodeInfo.get_con_usage_modify(con_id)
        con_data_handled = DataManage.manage_con_usage_info(con_data)
        self.render("node/con_modify.html", name=template_variables, single_con_usage_data = con_data_handled)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        con_dic = dict()
        for key in ['con_id', 'con_desc', 'con_app', 'user_name']:
            con_dic[key] = self.get_argument(key)
        con_ret = NodeInfo.set_con_usage_modify(con_dic)
        if con_ret == 0:
            url_cmd = ("<script language='javascript'>window.location.href='" +
                        "/conmanage?con_id=" + str(con_dic['con_id']) + "';</script>")
            self.write(url_cmd)
        else:
            self.write("<script language='javascript'>alert('修改失败');window.location.href='/conmanage';</script>")