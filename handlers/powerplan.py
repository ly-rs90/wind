#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@name: powerplan.py
@editor: PyCharm
@Date: 2019/3/13 10:01
@Author: ly
@Description: 
"""
import os
import json
from tornado.web import RequestHandler
from .e_file_model import *


class PowerPlan(RequestHandler):
    def post(self, *args, **kwargs):
        res_data = {
            'code': 0, 'msg': '', 'gen_cost': '', 'wind': '', 'spin': '', 'margin': '', 'conf': '',
            'wind_dev': [], 'power_dev': [], 'margin_dev': [], 'equ_dev': [], 'margin_opt': [],
            'margin_plb': [], 'margin_pub': [], 'margin_max': [], 'margin_min': [],
            'wind_opt': [], 'wind_plb': [], 'wind_pub': [], 'wind_fur': [], 'wind_cub': [], 'wind_clb': [],
            'power_opt': [], 'power_plb': [], 'power_pub': [], 'equ_opt': []
        }
        _date = self.get_argument('date')
        _type = self.get_argument('type', '')
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
            table_list = engine.getAllTableNames()
            if _type == 'basic':
                for tb in table_list:
                    table = engine.getTable(tb)
                    table_col_name = table.getAllColNames()
                    # col_num = table.getColNum()
                    # row_num = table.getRowNum()
                    if tb == 'sys':
                        gen_cost = table.getColumsData('gencost', table_col_name)  # 运行成本
                        wind = table.getColumsData('windcurtailcost', table_col_name)  # 弃风指标
                        spin = table.getColumsData('spin_reserve_value', table_col_name)  # 旋备指标
                        margin = table.getColumsData('tie_margin', table_col_name)  # 断面指标
                        conf = table.getColumsData('conf_prob', table_col_name)  # 置信区间
                        if gen_cost:
                            res_data['gen_cost'] = gen_cost[0]['data'][0]
                        if wind:
                            res_data['wind'] = wind[0]['data'][0]
                        if spin:
                            res_data['spin'] = spin[0]['data'][0]
                        if margin:
                            res_data['margin'] = margin[0]['data'][0]
                        if conf:
                            res_data['conf'] = conf[0]['data'][0]
                    elif tb == 'tie_crv':  # 断面信息
                        margin = table.getColumsData('name', table_col_name)
                        temp = set()
                        if margin:
                            margin = margin[0]['data']
                            for m in margin:
                                temp.add(m)
                        for m in temp:
                            res_data['margin_dev'].append({'value': m})
                    elif tb == 'statics_crv':    # 新能源和传统机组总加数据
                        statics = table.getColumsData('name', table_col_name)
                        for n in range(1, 169):
                            wind_opt = statics[2+n]['data'][0]     # 新能源优化设定值
                            wind_fur = statics[2+n]['data'][1]     # 新能源预测均值
                            wind_plb = statics[2+n]['data'][2]     # 新能源计划区间下限
                            wind_pub = statics[2+n]['data'][3]     # 新能源计划区间上限

                            power_opt = statics[2+n]['data'][4]     # 传统机组优化设定值
                            power_plb = statics[2+n]['data'][5]     # 传统机计划区间下限
                            power_pub = statics[2+n]['data'][6]     # 传统机计划区间上限

                            res_data['wind_opt'].append(wind_opt)
                            res_data['wind_fur'].append(wind_fur)
                            res_data['wind_plb'].append(wind_plb)
                            res_data['wind_pub'].append(wind_pub)

                            res_data['power_opt'].append(power_opt)
                            res_data['power_plb'].append(power_plb)
                            res_data['power_pub'].append(power_pub)
                    elif tb == 'unit_dev':      # 新能源和传统机组设备
                        unit_dev = table.getColumsData('type', table_col_name)
                        res_data['power_dev'].append({'value': '总和'})
                        res_data['wind_dev'].append({'value': '总和'})
                        for index, dev in enumerate(unit_dev[0]['data']):
                            if dev == '传统机组':
                                res_data['power_dev'].append({'value': unit_dev[1]['data'][index]})
                            if dev == '新能源机组':
                                res_data['wind_dev'].append({'value': unit_dev[1]['data'][index]})
                            if dev == '等值机组':
                                res_data['equ_dev'].append({'value': unit_dev[1]['data'][index]})
                    else:
                        continue
            elif _type == 'margin':     # 获取断面数据
                name = self.get_argument('name', '')
                margin_table = engine.getTable('tie_crv')
                table_col_name = margin_table.getAllColNames()
                margin_data = margin_table.getColumsData('name', table_col_name)

                dev_position = 0
                for index, v in enumerate(margin_data[0]['data']):
                    if v == name:
                        dev_position = index
                        break
                for n in range(1, 169):
                    # margin_data = margin_table.getColumsData(str(n), table_col_name)[0]['data']
                    # 优化设定值
                    opt = margin_data[2+n]['data'][dev_position]
                    # 计划下限
                    plb = margin_data[2+n]['data'][dev_position + 1]
                    # 计划上限
                    pub = margin_data[2+n]['data'][dev_position + 2]
                    # 上限
                    p_max = margin_data[2+n]['data'][dev_position + 3]
                    # 下限
                    p_min = margin_data[2+n]['data'][dev_position + 4]
                    res_data['margin_opt'].append(opt)
                    res_data['margin_plb'].append(plb)
                    res_data['margin_pub'].append(pub)
                    res_data['margin_max'].append(p_max)
                    res_data['margin_min'].append(p_min)
            elif _type == 'wind' or _type == 'power' or _type == 'equ':
                name = self.get_argument('name', '')
                unit_crt_table = engine.getTable('unit_crv')
                table_col_name = unit_crt_table.getAllColNames()
                unit_crt_data = unit_crt_table.getColumsData('name', table_col_name)

                dev_position = 0
                for index, v in enumerate(unit_crt_data[0]['data']):
                    if v == name:
                        dev_position = index
                        break

                if name == '总和' and _type == 'wind':
                    sum_data_tb = engine.getTable('statics_crv')
                    sum_col_name = sum_data_tb.getAllColNames()
                    sum_data = sum_data_tb.getColumsData('name', sum_col_name)
                    for m in range(1, 169):
                        wind_opt = sum_data[2 + m]['data'][0]  # 新能源优化设定值
                        wind_fur = sum_data[2 + m]['data'][1]  # 新能源预测均值
                        wind_plb = sum_data[2 + m]['data'][2]  # 新能源计划区间下限
                        wind_pub = sum_data[2 + m]['data'][3]  # 新能源计划区间上限

                        res_data['wind_opt'].append(wind_opt)
                        res_data['wind_fur'].append(wind_fur)
                        res_data['wind_plb'].append(wind_plb)
                        res_data['wind_pub'].append(wind_pub)
                elif name == '总和' and _type == 'power':
                    sum_data_tb = engine.getTable('statics_crv')
                    sum_col_name = sum_data_tb.getAllColNames()
                    sum_data = sum_data_tb.getColumsData('name', sum_col_name)

                    for m in range(1, 169):
                        power_opt = sum_data[2 + m]['data'][4]  # 传统机组优化设定值
                        power_plb = sum_data[2 + m]['data'][5]  # 传统机计划区间下限
                        power_pub = sum_data[2 + m]['data'][6]  # 传统机计划区间上限

                        res_data['power_opt'].append(power_opt)
                        res_data['power_plb'].append(power_plb)
                        res_data['power_pub'].append(power_pub)
                else:
                    for n in range(1, 169):
                        if _type == 'wind':
                            wind_opt = unit_crt_data[2+n]['data'][dev_position]
                            wind_pub = unit_crt_data[2+n]['data'][dev_position + 1]
                            wind_plb = unit_crt_data[2+n]['data'][dev_position + 2]
                            wind_cub = unit_crt_data[2+n]['data'][dev_position + 3]
                            wind_clb = unit_crt_data[2+n]['data'][dev_position + 4]
                            res_data['wind_opt'].append(wind_opt)
                            res_data['wind_pub'].append(wind_pub)
                            res_data['wind_plb'].append(wind_plb)
                            res_data['wind_cub'].append(wind_cub)
                            res_data['wind_clb'].append(wind_clb)
                        if _type == 'power':
                            power_opt = unit_crt_data[2 + n]['data'][dev_position]
                            power_pub = unit_crt_data[2 + n]['data'][dev_position + 1]
                            power_plb = unit_crt_data[2 + n]['data'][dev_position + 2]
                            res_data['power_opt'].append(power_opt)
                            res_data['power_pub'].append(power_pub)
                            res_data['power_plb'].append(power_plb)
                        if _type == 'equ':
                            equ_opt = unit_crt_data[2 + n]['data'][dev_position]
                            res_data['equ_opt'].append(equ_opt)
        self.write(json.dumps(res_data))