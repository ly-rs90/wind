#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@name: powerplan.py
@editor: PyCharm
@Date: 2019/3/13 10:01
@Author: ly
@Description: 
"""
import json
from tornado.web import RequestHandler
from .efile import EFile


class PowerPlan(RequestHandler):
    def post(self, *args, **kwargs):
        res_data = {
            'code': 0, 'msg': '', 'gen_cost': '', 'wind': '', 'spin': '', 'margin': '', 'conf': '',
            'wind_dev': [], 'power_dev': [], 'margin_dev': [], 'equ_dev': [], 'margin_opt': [],
            'margin_plb': [], 'margin_pub': [], 'margin_max': [], 'margin_min': [],
            'wind_opt': [], 'wind_plb': [], 'wind_pub': [], 'wind_fur': [], 'wind_cub': [], 'wind_clb': [],
            'power_opt': [], 'power_plb': [], 'power_pub': [], 'equ_opt': [], 'agc_dev': []
        }
        _date = self.get_argument('date')
        _type = self.get_argument('type', '')

        e_file = EFile(f'uc_plan_{_date}.txt')

        if _type == 'basic':
            # ***系统信息***
            sys_tb = e_file.tables.get('sys')
            sys_data = e_file.get_table('sys')
            if sys_data:
                for i, v in enumerate(sys_tb):
                    # 运行成本
                    if v == 'gencost':
                        res_data['gen_cost'] = sys_data[0][i]
                    # 弃风指标
                    if v == 'windcurtailcost':
                        res_data['wind'] = sys_data[0][i]
                    # 旋备指标
                    if v == 'spin_reserve_value':
                        res_data['spin'] = sys_data[0][i]
                    # 断面指标
                    if v == 'tie_margin':
                        res_data['margin'] = sys_data[0][i]
                    # 置信区间
                    if v == 'conf_prob':
                        res_data['conf'] = sys_data[0][i]

            # *** end ***

            # ***设备***
            # 断面设备
            tie = e_file.get_table('tie_crv')
            temp = set()
            for m in tie:
                temp.add(m[0])

            for m in temp:
                res_data['margin_dev'].append({'value': m})

            # 机组
            res_data['power_dev'].append({'value': '总和'})
            res_data['wind_dev'].append({'value': '总和'})
            res_data['agc_dev'].append({'value': '总和'})
            wind = e_file.get_table('unit_dev', type='新能源机组')
            power = e_file.get_table('unit_dev', type='传统机组')
            agc = e_file.get_table('unit_dev', type='AGC机组')
            equ = e_file.get_table('unit_dev', type='等值机组')
            for w in wind:
                res_data['wind_dev'].append({'value': w[0]})
            for p in power:
                res_data['power_dev'].append({'value': p[0]})
            for a in agc:
                res_data['agc_dev'].append({'value': a[0]})
            for e in equ:
                res_data['equ_dev'].append({'value': e[0]})
            # *** end ***

            # ***新能源设备，传统机组，AGC机组总和***
            # 新能源优化设定值
            wind_opt = e_file.get_table('statics_crv', name='新能源机组总和', type='popt')
            # 新能源预测均值
            wind_fur = e_file.get_table('statics_crv', name='新能源机组总和', type='pfur')
            # 新能源计划区间下限
            wind_plb = e_file.get_table('statics_crv', name='新能源机组总和', type='plb')
            # 新能源计划区间上限
            wind_pub = e_file.get_table('statics_crv', name='新能源机组总和', type='pub')

            # 传统机组优化设定值
            power_opt = e_file.get_table('statics_crv', name='传统机组总和', type='popt')
            # 传统机计划区间下限
            power_plb = e_file.get_table('statics_crv', name='传统机组总和', type='plb')
            # 传统机计划区间上限
            power_pub = e_file.get_table('statics_crv', name='传统机组总和', type='pub')

            # AGC机组优化设定值
            agc_opt = e_file.get_table('statics_crv', name='AGC机组总和', type='popt')
            # AGC机组计划区间下限
            agc_plb = e_file.get_table('statics_crv', name='AGC机组总和', type='plb')
            # AGC机组计划区间上限
            agc_pub = e_file.get_table('statics_crv', name='AGC机组总和', type='pub')

            res_data['wind_opt'] = wind_opt[0][2:] if wind_opt else []
            res_data['wind_fur'] = wind_fur[0][2:] if wind_fur else []
            res_data['wind_plb'] = wind_plb[0][2:] if wind_plb else []
            res_data['wind_pub'] = wind_pub[0][2:] if wind_pub else []

            res_data['power_opt'] = power_opt[0][2:] if power_opt else []
            res_data['power_plb'] = power_plb[0][2:] if power_plb else []
            res_data['power_pub'] = power_pub[0][2:] if power_pub else []

            res_data['agc_opt'] = agc_opt[0][2:] if agc_opt else []
            res_data['agc_plb'] = agc_plb[0][2:] if agc_plb else []
            res_data['agc_pub'] = agc_pub[0][2:] if agc_pub else []
            # *** end ***
        elif _type == 'margin':
            # 断面数据

            name = self.get_argument('name', '')

            # 优化设定值
            opt = e_file.get_table('tie_crv', name=name, type='popt')
            # 计划下限
            plb = e_file.get_table('tie_crv', name=name, type='plb')
            # 计划上限
            pub = e_file.get_table('tie_crv', name=name, type='pub')
            # 上限
            p_max = e_file.get_table('tie_crv', name=name, type='pmax')
            # 下限
            p_min = e_file.get_table('tie_crv', name=name, type='pmin')

            res_data['margin_opt'] = opt[0][2:] if opt else []
            res_data['margin_plb'] = plb[0][2:] if plb else []
            res_data['margin_pub'] = pub[0][2:] if pub else []
            res_data['margin_max'] = p_max[0][2:] if p_max else []
            res_data['margin_min'] = p_min[0][2:] if p_min else []

        elif _type in ('wind', 'power', 'equ', 'agc'):
            name = self.get_argument('name', '')

            if name == '总和' and _type == 'wind':
                for m in range(1, 169):
                    # 新能源优化设定值
                    wind_opt = e_file.get_table('statics_crv', name='新能源机组总和', type='popt')
                    # 新能源预测均值
                    wind_fur = e_file.get_table('statics_crv', name='新能源机组总和', type='pfur')
                    # 新能源计划区间下限
                    wind_plb = e_file.get_table('statics_crv', name='新能源机组总和', type='plb')
                    # 新能源计划区间上限
                    wind_pub = e_file.get_table('statics_crv', name='新能源机组总和', type='pub')

                    res_data['wind_opt'] = wind_opt[0][2:] if wind_opt else []
                    res_data['wind_fur'] = wind_fur[0][2:] if wind_fur else []
                    res_data['wind_plb'] = wind_plb[0][2:] if wind_plb else []
                    res_data['wind_pub'] = wind_pub[0][2:] if wind_pub else []
            elif name == '总和' and _type == 'power':
                # 传统机组优化设定值
                power_opt = e_file.get_table('statics_crv', name='传统机组总和', type='popt')
                # 传统机计划区间下限
                power_plb = e_file.get_table('statics_crv', name='传统机组总和', type='plb')
                # 传统机计划区间上限
                power_pub = e_file.get_table('statics_crv', name='传统机组总和', type='pub')

                res_data['power_opt'] = power_opt[0][2:] if power_opt else []
                res_data['power_plb'] = power_plb[0][2:] if power_plb else []
                res_data['power_pub'] = power_pub[0][2:] if power_pub else []

            elif name == '总和' and _type == 'agc':
                # AGC机组优化设定值
                agc_opt = e_file.get_table('statics_crv', name='AGC机组总和', type='popt')
                # AGC机计划区间下限
                agc_plb = e_file.get_table('statics_crv', name='AGC机组总和', type='plb')
                # AGC机计划区间上限
                agc_pub = e_file.get_table('statics_crv', name='AGC机组总和', type='pub')

                res_data['agc_opt'] = agc_opt[0][2:] if agc_opt else []
                res_data['agc_plb'] = agc_plb[0][2:] if agc_plb else []
                res_data['agc_pub'] = agc_pub[0][2:] if agc_pub else []
            else:
                if _type == 'power':
                    opt = e_file.get_table('unit_crv', name=name, type='popt')  # 优化设定值
                    pub = e_file.get_table('unit_crv', name=name, type='ppub')  # 计划区间上限
                    plb = e_file.get_table('unit_crv', name=name, type='pplb')  # 计划区间下限
                    fur = e_file.get_table('unit_crv', name=name, type='pfur')  # 预测值

                    res_data['power_opt'] = opt[0][2:] if opt else []
                    res_data['power_pub'] = pub[0][2:] if pub else []
                    res_data['power_plb'] = plb[0][2:] if plb else []
                    res_data['power_fur'] = fur[0][2:] if fur else []
                elif _type == 'equ':
                    opt = e_file.get_table('unit_crv', name=name, type='popt')  # 优化设定值
                    fur = e_file.get_table('unit_crv', name=name, type='pfur')  # 预测值

                    res_data['equ_opt'] = opt[0][2:] if opt else []
                    res_data['equ_fur'] = fur[0][2:] if fur else []
                elif _type == 'agc':
                    # 优化设定值
                    agc_opt = e_file.get_table('unit_crv', name=name, type='popt')
                    # 计划上限
                    agc_pub = e_file.get_table('unit_crv', name=name, type='ppub')
                    # 计划下限
                    agc_plb = e_file.get_table('unit_crv', name=name, type='pplb')
                    # 预测上限
                    agc_cub = e_file.get_table('unit_crv', name=name, type='pcub')
                    # 预测下限
                    agc_clb = e_file.get_table('unit_crv', name=name, type='pclb')
                    # 预测值
                    agc_fur = e_file.get_table('unit_crv', name=name, type='pfur')

                    res_data['agc_opt'] = agc_opt[0][2:] if agc_opt else []
                    res_data['agc_pub'] = agc_pub[0][2:] if agc_pub else []
                    res_data['agc_plb'] = agc_plb[0][2:] if agc_plb else []
                    res_data['agc_cub'] = agc_cub[0][2:] if agc_cub else []
                    res_data['agc_clb'] = agc_clb[0][2:] if agc_clb else []
                    res_data['agc_fur'] = agc_fur[0][2:] if agc_fur else []
                elif _type == 'wind':
                    # 优化设定值
                    wind_opt = e_file.get_table('unit_crv', name=name, type='popt')
                    # 计划上限
                    wind_pub = e_file.get_table('unit_crv', name=name, type='ppub')
                    # 计划下限
                    wind_plb = e_file.get_table('unit_crv', name=name, type='pplb')
                    # 预测上限
                    wind_cub = e_file.get_table('unit_crv', name=name, type='pcub')
                    # 预测下限
                    wind_clb = e_file.get_table('unit_crv', name=name, type='pclb')
                    # 预测值
                    wind_fur = e_file.get_table('unit_crv', name=name, type='pfur')

                    res_data['wind_opt'] = wind_opt[0][2:] if wind_opt else []
                    res_data['wind_pub'] = wind_pub[0][2:] if wind_pub else []
                    res_data['wind_plb'] = wind_plb[0][2:] if wind_plb else []
                    res_data['wind_cub'] = wind_cub[0][2:] if wind_cub else []
                    res_data['wind_clb'] = wind_clb[0][2:] if wind_clb else []
                    res_data['wind_fur'] = wind_fur[0][2:] if wind_fur else []


        self.write(json.dumps(res_data))