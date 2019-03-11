#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .e_file_parse import *

class EFileTableModel:
    """
    EFile Data Model
    """
    def __init__(self,name,moduleInfo):
        self.name =name
        self.moduleInfo = moduleInfo

    def getAllColNames(self):
        return self.moduleInfo.getColNames()
    def getRowNum(self):
        return self.moduleInfo.getRowNum()
    def getColNum(self):
        return self.moduleInfo.getColNum()
    def getColumsData(self,keyColName,colNameLst):
        rowNum = self.getRowNum()
        if keyColName.strip() == '' or rowNum <= 0 or self.getColNum() <= 0 :
            return []
        keyIndex = self.moduleInfo.getColIndexByName(keyColName)
        if -1 == keyIndex:
            print("keyColName[%s] not found!" % keyColName)
            return []
        try:
            queryDatas = []
            queryColLst = [keyColName]
            if type(colNameLst) is str:
                queryColLst.append(colNameLst)
            elif type(colNameLst) is list:
                queryColLst.extend(colNameLst)
            else:
                print("keyColName type error!")
                return queryDatas
            qColNum = len(queryColLst)
            for tmpColName in queryColLst:
                icol = self.getAllColNames().index(tmpColName)
                colDataObj = []
                colObj = {'name': tmpColName, 'data': colDataObj}
                queryDatas.append(colObj)
                for tmpRow in self.moduleInfo.rowLst:
                    colDataObj.append(tmpRow[icol])

        except (AttributeError, ValueError) as e:
            print(e)
        except:
            print("Some error happens, in RTDBTableModel::getColumsData")
        else:
            pass
        return queryDatas
    
class EFileEngine:
    def __init__(self):
        self.parser = EFileParse()
    def LoadFile(self,fileName):
        self.tableNameLst = []
        bSuc = self.parser.readFile(fileName)
        if not bSuc:
            return False
        return True
    def getAllTableNames(self):
        return self.parser.moduleNameLst
    def getTable(self,tableName):
        if tableName.strip() =='':
            return None
        tmpModule = self.parser.getModuleByName(tableName)
        if not tmpModule:
            return None
        return EFileTableModel(tableName,tmpModule)

if __name__ == "__main__":
    #efile
    engine = EFileEngine()
    bSuc = engine.LoadFile('efile_test.dt')
    if not bSuc:
        exit(0)
    tbLst = engine.getAllTableNames()
    for tbName in tbLst:
        tb = engine.getTable(tbName)
        tmpColLst = tb.getAllColNames()
        print(tb.getColNum())
        print(tb.getRowNum())
        tmpObj = tb.getColumsData(tmpColLst[0],tmpColLst)
        print(tmpObj)
