#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@name: devplan.py
@editor: PyCharm
@Date: 2019/3/12 11:01
@Author: ly
@Description: 
"""
import os
import json
from tornado.web import RequestHandler
from .e_file_model import *


class DevPlan(RequestHandler):
    def post(self, *args, **kwargs):
        res_data = {'code': 0, 'msg': '', 'data': {}, 'gen_cost': '', 'wind': '', 'spin': '', 'margin': ''}
        _date = self.get_argument('date')
        file_name = 'uc_plan_{}.txt'.format(_date)

        cur_path = os.path.dirname(__file__)
        root_path = os.path.dirname(cur_path)
        e_file_path = os.path.join(root_path, 'efiles')

        engine = EFileEngine()
        flag = engine.LoadFile(os.path.join(e_file_path, file_name))
        if not flag:
            res_data['code'] = 1
            res_data['msg'] = '加载e文件失败！'
        else:
            sys_table = engine.getTable('sys')
            table_col_name = sys_table.getAllColNames()
            gen_cost = sys_table.getColumsData('gencost', table_col_name)  # 运行成本
            wind = sys_table.getColumsData('windcurtailcost', table_col_name)  # 弃风指标
            spin = sys_table.getColumsData('spin_reserve_value', table_col_name)  # 旋备指标
            margin = sys_table.getColumsData('tie_margin', table_col_name)  # 断面指标

            if gen_cost:
                res_data['gen_cost'] = gen_cost[0]['data'][0]
            if wind:
                res_data['wind'] = wind[0]['data'][0]
            if spin:
                res_data['spin'] = spin[0]['data'][0]
            if margin:
                res_data['margin'] = margin[0]['data'][0]

            unit_table = engine.getTable('unit_uc')
            table_col_name = unit_table.getAllColNames()
            unit_data = unit_table.getColumsData('name', table_col_name)
            dev_len = len(unit_data[0]['data'])
            dev_data = []
            for n in range(dev_len):
                dev_data.append([])
            for n in range(168):
                data = unit_data[n+2]['data']
                for index, v in enumerate(data):
                    dev_data[index].append(v)
            for index, v in enumerate(unit_data[0]['data']):
                res_data['data'][v] = dev_data[index]
        self.write(json.dumps(res_data))
