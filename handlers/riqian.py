#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@name: riqian.py
@editor: PyCharm
@Date: 2019/1/18 10:06
@Author: ly
@Description: 
"""
import json
from tornado.web import RequestHandler
from .efile import EFile


class Riqian(RequestHandler):
    def post(self, *args, **kwargs):
        res_data = {
            'code': 0, 'msg': '', 'gen_cost': '', 'wind': '', 'spin': '', 'margin': '', 'conf': '',
            'wind_dev': [], 'power_dev': [], 'margin_dev': [], 'equ_dev': [], 'margin_opt': [],
            'margin_plb': [], 'margin_pub': [], 'margin_max': [], 'margin_min': [],
            'wind_opt': [], 'wind_plb': [], 'wind_pub': [], 'wind_fur': [], 'wind_cub': [], 'wind_clb': [],
            'power_opt': [], 'power_plb': [], 'power_pub': [], 'equ_opt': [], 'start': 1, 'end': 96, 'interval': 15,
            'es_dev': [], 'es_opt': [], 'es_cap': [], 'agc_dev': []
        }
        _date = self.get_argument('date')
        _type = self.get_argument('type', '')
        e_file = EFile(f'dh_plan_{_date}.txt')

        if _type == 'basic':
            # ***系统信息**
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
                    if v == 'start_pt':
                        res_data['start'] = int(sys_data[0][i])
                    if v == 'end_pt':
                        res_data['end'] = int(sys_data[0][i])
                    if v == 'mins':
                        res_data['interval'] = int(sys_data[0][i])
            # *** end ***

            # ***断面设备***
            tie = e_file.get_table('tie_crv')
            temp = set()
            for t in tie:
                temp.add(t[0])
            for m in temp:
                res_data['margin_dev'].append({'value': m})
            # *** end ***

            # ***总加数据***
            ## 新能源
            # 新能源优化设定值
            wind_opt = e_file.get_table('statics_crv', name='新能源机组总和', type='popt')
            # 新能源预测均值
            wind_fur = e_file.get_table('statics_crv', name='新能源机组总和', type='pfur')
            # 新能源计划区间下限
            wind_plb = e_file.get_table('statics_crv', name='新能源机组总和', type='plb')
            # 新能源计划区间上限
            wind_pub = e_file.get_table('statics_crv', name='新能源机组总和', type='pub')

            ## 传统机组
            # 传统机组优化设定值
            power_opt = e_file.get_table('statics_crv', name='传统机组总和', type='popt')
            # 传统机计划区间下限
            power_plb = e_file.get_table('statics_crv', name='传统机组总和', type='plb')
            # 传统机计划区间上限
            power_pub = e_file.get_table('statics_crv', name='传统机组总和', type='pub')

            ## AGC机组
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

            # ***机组设备***
            res_data['power_dev'].append({'value': '总和'})
            res_data['wind_dev'].append({'value': '总和'})
            res_data['agc_dev'].append({'value': '总和'})

            dev = e_file.get_table('unit_dev')
            for d in dev:
                if d[1] == '传统机组':
                    res_data['power_dev'].append({'value': d[0]})
                if d[1] == '新能源机组':
                    res_data['wind_dev'].append({'value': d[0]})
                if d[1] == '等值机组':
                    res_data['equ_dev'].append({'value': d[0]})
                if d[1] == 'AGC机组':
                    res_data['agc_dev'].append({'value': d[0]})
            # *** end ***

            # ***储能设备***
            es = e_file.get_table('es_crv')
            temp = set()
            for e in es:
                temp.add(e[0])
            for name in temp:
                res_data['es_dev'].append({'value': name})
            # *** end ***
        elif _type == 'margin':
            name = self.get_argument('name', '')
            ## 断面数据

            # 优化设定值
            opt = e_file.get_table('tie_crv', name=name, type='popt')
            # 计划下限
            plb = e_file.get_table('tie_crv', name=name, type='plb')
            # 计划上限
            pub = e_file.get_table('tie_crv', name=name, type='pub')
            # 上限
            p_max = e_file.get_table('tie_crv', name=name, type='pmax')
            # 下限
            p_min = e_file.get_table('tie_crv', name=name, type='pmax')

            res_data['margin_opt'] = opt[0][2:] if opt else []
            res_data['margin_plb'] = plb[0][2:] if plb else []
            res_data['margin_pub'] = pub[0][2:] if pub else []
            res_data['margin_max'] = p_max[0][2:] if p_max else []
            res_data['margin_min'] = p_min[0][2:] if p_min else []
        elif _type == 'es':
            # 储能
            name = self.get_argument('name', '')

            # 优化设定值
            opt = e_file.get_table('es_crv', name=name, type='popt')
            # 容量
            cap = e_file.get_table('es_crv', name=name, type='cap')

            res_data['es_opt'] = opt[0][2:] if opt else []
            res_data['es_cap'] = cap[0][2:] if cap else []
        elif _type in ('wind', 'power', 'equ', 'agc'):
            name = self.get_argument('name', '')

            if name == '总和' and _type == 'wind':
                ## 新能源
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
                ## 传统机组
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
                ## AGC机组
                # AGC机组优化设定值
                agc_opt = e_file.get_table('statics_crv', name='AGC机组总和', type='popt')
                # AGC机组计划区间下限
                agc_plb = e_file.get_table('statics_crv', name='AGC机组总和', type='plb')
                # AGC机组计划区间上限
                agc_pub = e_file.get_table('statics_crv', name='AGC机组总和', type='pub')

                res_data['agc_opt'] = agc_opt[0][2:] if agc_opt else []
                res_data['agc_plb'] = agc_plb[0][2:] if agc_plb else []
                res_data['agc_pub'] = agc_pub[0][2:] if agc_pub else []
            else:
                if _type == 'power':
                    power_opt = e_file.get_table('unit_crv', name=name, type='popt')
                    power_pub = e_file.get_table('unit_crv', name=name, type='ppub')
                    power_plb = e_file.get_table('unit_crv', name=name, type='pplb')

                    res_data['power_opt'] = power_opt[0][2:] if power_opt else []
                    res_data['power_pub'] = power_pub[0][2:] if power_pub else []
                    res_data['power_plb'] = power_plb[0][2:] if power_plb else []
                elif _type == 'equ':
                    # 等值机组
                    equ = e_file.get_table('unit_crv', name=name, type='popt')
                    res_data['equ_opt'] = equ[0][2:] if equ else []
                elif _type == 'wind':
                    # 新能源
                    wind_opt = e_file.get_table('unit_crv', name=name, type='popt')
                    wind_pub = e_file.get_table('unit_crv', name=name, type='ppub')
                    wind_plb = e_file.get_table('unit_crv', name=name, type='pplb')
                    wind_cub = e_file.get_table('unit_crv', name=name, type='pcub')
                    wind_clb = e_file.get_table('unit_crv', name=name, type='pclb')

                    res_data['wind_opt'] = wind_opt[0][2:] if wind_opt else []
                    res_data['wind_pub'] = wind_pub[0][2:] if wind_pub else []
                    res_data['wind_plb'] = wind_plb[0][2:] if wind_plb else []
                    res_data['wind_cub'] = wind_cub[0][2:] if wind_cub else []
                    res_data['wind_clb'] = wind_clb[0][2:] if wind_clb else []
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


        self.write(json.dumps(res_data))
