#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@name: efile.py
@editor: PyCharm
@Date: 2019/7/1 15:09
@Author: ly
@Description: 本模块提供对e文件条件查询功能
"""
import os
from .e_file_model import *


class EFile:
    """efile查询方法封装类"""
    def __init__(self, file_name):
        self._file = file_name
        self._eg = self._load_file()
        self._tables = self._get_tables()
        self._all_data = self._get_all_data()

    def _load_file(self):
        """加载efile，如果成功返回一个engine实列否则返回None"""
        cur_path = os.path.dirname(__file__)
        root_path = os.path.dirname(cur_path)
        e_file_path = os.path.join(root_path, 'efiles')

        eg = EFileEngine()
        f = eg.LoadFile(os.path.join(e_file_path, self._file))
        if f:
            return eg
        else:
            return None

    def _get_tables(self):
        """获取文件中所有表和表对应的所有列"""
        tbs = {}
        if self._eg:
            table_name_list = self._eg.getAllTableNames()
            for t in table_name_list:
                table = self._eg.getTable(t)
                col_names = table.getAllColNames()
                tbs[t] = col_names
        return tbs

    def _get_all_data(self):
        """获取表数据"""
        data = {}
        for key in self._tables:
            data[key] = []
            table = self._eg.getTable(key)
            table_data = table.getColumsData(self._tables[key][0], self._tables[key])
            if  not table_data:
                continue
            col_len = len(table_data) - 1
            row_num = len(table_data[0]['data'])
            for n in range(row_num):
                row_data = []
                for m in range(1, col_len + 1):
                    row_data.append(table_data[m]['data'][n])
                data[key].append(row_data)
        return data

    def get_table(self, tb, **param):
        data = []
        if tb not in self._tables:
            return data
        for key in param:
            if key not in self._tables[tb]:
                return data

        condition = {}
        for key in param:
            for n, v in enumerate(self._tables[tb]):
                if v == key:
                    condition[n] = param[key]

        if not condition:
            return self._all_data[tb]

        for n in self._all_data[tb]:
            for key in condition:
                if n[key] != condition[key]:
                    break
            else:
                data.append(n)
        return data

    @property
    def tables(self):
        return self._tables
