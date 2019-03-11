#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,re
import codecs

def praseLine(lineStr):
    valLst = []
    lineStr = lineStr.strip()
    if lineStr == '':
        return valLst
    reObj = re.search(r"'+\w*\s*\w*'+", lineStr)
    if not reObj:
        return re.split(r'\s+',lineStr)
    else:
        tmpStr = reObj.group()
        tmpIndex = lineStr.index(tmpStr)
        valLst.extend(re.split(r'\s+',lineStr[:tmpIndex].strip()))
        valLst.append(tmpStr)
        valLst.extend(praseLine(lineStr[tmpIndex + len(tmpStr):len(lineStr)]))
        return valLst


class EFileModuleInfo:
    def __init__(self,descStr):
        self.desc = descStr
        self.colNames = []
        self.rowLst = []
        self.propDict = {}
        self.hasModified = False
    def clear(self):
        self.colNames = []
        self.rowLst = []
        self.propDict = {}

    def addProp(self,propName,propVal):
        self.propDict[propName] = propVal
    def loadModule(self,fileObj):
        self.clear()
        self.hasModified = False
        line = "hi"
        while line:
            line = fileObj.readline()
            if not line:
                break
            tmpline = line.strip()
            if len(tmpline) < 2:
                continue
            dataStr = tmpline[1:].strip()
            if tmpline[0] == '@':
                self.colNames.extend(praseLine(dataStr))
            elif tmpline[0] == '#':
                self.rowLst.append(praseLine(dataStr))
            elif tmpline[:2] == '//':
                continue
            elif tmpline[0] == '<':
                if tmpline[1] == '!':
                    continue
                return True
            else:
                print("error line:%s"% line)
                return False
        return True
    def writeFile(self,fileObj):
        try:
            fileObj.write("@")
            for tmpCol in self.colNames:
                fileObj.write(" %s " % tmpCol)
            fileObj.write("\n")
            for tmpRow in self.rowLst:
                fileObj.write("# %s\n" % " ".join(tmpRow))
            fileObj.flush()
        except IOError as e:
            print(e)
        except:
            print("some unkown error")
        else:
            return True
        return False

    def getColNames(self):
        return self.colNames
    def getColIndexByName(self, colName):
        try:
            index  = self.colNames.index(colName)
        except ValueError as e:
            print(e)
        except:
            print("some unkown error")
        else:
            return index
        return -1

    def getColByIndex(self,icol):
        '''
        @descript
        @return
        '''
        colLst = []
        colNum = len(self.colNames)
        if icol >= colNum:
            return colLst
        for tmpRow in self.rowLst:
            if icol >= len(tmpRow):
                colLst.append('')
                continue
            colLst.append(tmpRow[icol])
        return colLst
    def getColByName(self,colName):
        try:
            index = self.colNames.index(colName)
        except ValueError as e:
            print(e)
            return None
        else:
            return self.getColByIndex(index)
    def getRowNum(self):
        return len(self.rowLst)
    def getColNum(self):
        if self.getRowNum() <= 0:
            return 0
        return len(self.rowLst[0])
    def getRowByIndex(self,irow):
        try:
            tmpRow = self.rowLst[irow]
        except IndexError as e:
            print(e)
            return None
        else:
            return tmpRow

    def setColName(self,colIndex,newName):
        try:
            self.colNames[colIndex] = newName
        except IndexError as e:
            print(e)
            return False
        else:
            return True
    def renameCol(self,oldName,newName):
        try:
            colIndex = self.colNames.index(oldName)
        except ValueError as e:
            print(e)
            return None
        else:
            return self.setColName(colIndex,newName)
    def getCellVal(self,iRow,iCol):
        try:
            tmpRow = self.rowLst[iRow]
        except IndexError as e:
            print("row index [%d] error:%s"%(iRow,e))
        except:
            print("some error happend!")
        else:
            try:
                tmpVal = tmpRow[iCol]
            except IndexError as e:
                print("col index [%d] error:%s" % (iCol,e))
            except:
                print("some error happend!")
            else:
                return tmpVal
        return None
    def setCellVal(self,iRow,iCol,newVal):
        try:
            tmpRow = self.rowLst[iRow]
        except IndexError as e:
            print("row index [%d] error:%s"%(iRow,e))
        except:
            print("some error happens!")
        else:
            try:
                tmpRow[iCol] = newVal
            except IndexError as e:
                print("col index [%d] error:%s" % (iCol,e))
            except:
                print("some error happens!")
            else:
                return True
        return False


class EFileParse:
    '''
    E file Read and Write.
    '''
    def __init__(self):
        self.headerNameToVal = {}
        self.moduleNameLst = []
        self.moduleDict= {}
    
    def readFile(self,fileName):
        self.headerNameToVal = {}
        self.moduleNameLst = []
        self.moduleDict= {}
        if not os.path.exists(fileName):
            print("文件不存在：%s" % fileName)
            return False
        file_object = codecs.open(fileName,'r','gb18030')
        try:
            tmpline = 'hi'
            while tmpline:
                tmpline = file_object.readline()
                line = tmpline.strip()
                if len(line) < 2:
                    continue
                if line[0] == '<':
                    if line[1] == '!':
                        self.parseHeader(line[2:])
                    elif line[1] == '/':
                        continue
                    else:
                        self.praseModule(line,file_object)
        finally:
            file_object.close()
        return True

    def parseHeader(self,headerStr):
        for tmpStr in re.split('\s+',headerStr.strip()):
            tmpLst = tmpStr.split('=')
            if len(tmpLst) != 2:
                continue
            self.headerNameToVal[tmpLst[0]] = tmpLst[1]
        return True
    def AddModule(self,descStr):
        tmpLst = descStr.split('::')
        tmpDesc = ''
        if len(tmpLst) < 1:
            return None
        elif len(tmpLst) >= 2:
            tmpDesc = tmpLst[1]
        newModule = EFileModuleInfo(tmpDesc)
        self.moduleDict[tmpLst[0]]=newModule
        self.moduleNameLst.append(tmpLst[0])
        return newModule
    def praseModule(self,descStr,file_object):
        endIndex = descStr.find('>')
        if endIndex == -1:
            return False
        descStr = descStr[1:endIndex].strip()
        tmpPropLst = re.split('\s+', descStr)
        newModule = self.AddModule(tmpPropLst[0])
        if len(tmpPropLst) >= 1:
            for tmpProp in tmpPropLst[1:]:
                tmpLst = tmpProp.split('=')
                if len(tmpLst) != 2:
                    continue
                newModule.addProp(tmpLst[0],tmpLst[1])
        return newModule.loadModule(file_object)
    def writeFile(self,fileName):
        fileObj = codecs.open(fileName,'w','gb18030')
        #fileObj = open(fileName,'w')
        try:
            szEntity = ''
            if len(self.headerNameToVal) > 0:
                fileObj.write("<!")
                for key,val in self.headerNameToVal.items():
                    fileObj.write(" %s=%s " % (key,val))
                    if key == "Entity":
                        szEntity = val
                fileObj.write(">\n")
                fileObj.flush()
            if len(self.moduleDict) > 0:
                for key,val in self.moduleDict.items():
                    descStr = val.desc
                    if descStr.strip() == '':
                        descStr = szEntity
                    fileObj.write("<%s::%s" % (key,descStr))
                    if len(val.propDict) > 0:
                        for propName,propVal in val.propDict:
                            fileObj.write(" %s=%s " % (propName,propVal))
                        fileObj.write(">\n")
                    val.writeFile(fileObj)
                    fileObj.write("</%s>\n"% key)
                    fileObj.flush()
        except IOError as e:
            print(e)
            return False
        except:
            print("some unkown happens!")
        else:
            return True
        fileObj.close()
    def getHeadMap(self):
        return self.headerNameToVal
    def getAllModuleName(self):
        return self.moduleNameLst
    def getModuleNum(self):
        return len(self.moduleNameLst)

    def getModuleByIndex(self,index):
        '''
        @descript
        @ param index the index of moudule
        @return
        '''
        if self.getModuleNum() <= index:
            return None
        moduleName = self.moduleNameLst[index]
        return moduleName,self.moduleDict[moduleName]
    def getModuleByName(self,moduleName):
        if not (moduleName in self.moduleDict):
            return None
        return self.moduleDict[moduleName]



if __name__ == "__main__":
    tmpStr = "hi 'h i' hi2 ' ' hello '' world"
    mylist = praseLine(tmpStr)
    parseObj = EFileParse()
    parseObj.readFile('FLOWGATE.DT')

    tmpName,tmpObj = parseObj.getModuleByIndex(0)
    print (tmpName,tmpObj)
    #print(parseObj.getModuleByName(tmpName))
    #print(tmpObj.getColByName('time2'))
    print(tmpObj.getRowByIndex(2))
    print(tmpObj.getCellVal(2,1))
    parseObj.writeFile("test.txt")
