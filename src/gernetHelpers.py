import json
import re
import os

DefaultMapBuffer = 'com.github.airutech.cnets.mapBuffer'

def readJson(filename):
    json_file_to_read = os.path.join(filename)
    read_data = None
    with open (json_file_to_read, "r") as jsonfile:
        pat=re.compile(r'/\*.*?\*/',re.DOTALL|re.M)
        json_data = re.sub(pat, '', jsonfile.read())
        try:
            read_data = json.loads(json_data)
        except:
            print json_file_to_read+" invalid"
            jsonfile.close()
            raise
        jsonfile.close()
    return read_data

def filterTypes_java(t):
    serializableType = False
    isObject = True
    isArray = False
    if len(t)>2 and t[-2:] == '[]':
        isArray = True
        t = t[:-2]
    if t in ["string","String"]:
        t = "String"
        serializableType = True
    if t in ["char","Char"]:
        t = "char" if isArray else "char"
        isObject = False
        serializableType = True
    if t in ["int","Integer"]:
        t = "int" if isArray else "int"
        isObject = False
        serializableType = True
    if t in ["unsigned","long","Long"]:
        t = "long" if isArray else "long"
        isObject = False
        serializableType = True
    if t in ["boolean", "Boolean"]:
        t = "boolean" if isArray else "boolean"
        isObject = False
        serializableType = True
    if t in ["double","Double"]:
        t = "double" if isArray else "double"
        isObject = False
        serializableType = True
    if t in ["float","Float"]:
        t = "float" if isArray else "float"
        isObject = False
        serializableType = True
    if t in ["Object"]:
        t = "Object"
    if isArray:
        t += "[]"
        isObject = True
    return t, isObject, isArray, serializableType

def filterTypes_c(t):
    serializableType = False
    isObject = True
    isArray = False
    if len(t)>2 and t[-2:] == '[]':
        isArray = True
        t = t[:-2]
    if t in ["string","String","char*"]:
        t = "char*"
        serializableType = True
    if t in ["char","Char"]:
        t = "char"
        isObject = False
        serializableType = True
    if t in ["int","Integer"]:
        t = "int32_t"
        isObject = False
        serializableType = True
    if t in ["unsigned"]:
        t = "uint32_t"
        isObject = False
        serializableType = True
    if t  in ["long","Long"]:
        t = "int64_t"
        isObject = False
        serializableType = True
    if t in ["boolean", "Boolean"]:
        t = "BOOL" if isArray else "BOOL"
        isObject = False
        serializableType = True
    if t in ["double","Double"]:
        t = "double"
        isObject = False
        serializableType = True
    if t in ["float","Float"]:
        t = "float"
        isObject = False
        serializableType = True
    if t in ["Object"]:
        t = "void*"
    if isArray:
        t = "arrayObject"
        isObject = True
    return t, isObject, isArray, serializableType


def getClassName(path):
    fullNameList = path.split('.')
    return fullNameList[-1]

def getCompany(path):
    fullNameList = path.split('.')
    return fullNameList[1]

def getCompanyDomain(path):
    fullNameList = path.split('.')
    return fullNameList[1]+'.'+fullNameList[0]

def getDomainName(path):
    fullNameList = path.split('.')
    del fullNameList[-1]
    return '.'.join(fullNameList)

def getDomainPath(path):
    fullNameList = path.split('.')
    to_delete = [0,1]
    for offset, index in enumerate(to_delete):
        index -= offset
        del fullNameList[index]
    return getCompanyDomain(path)+'/'+('/'.join(fullNameList))

def getFullName_(path):
    return '_'.join(path.split('.'))

def getRootPath(path):
    countstepsup = len(path.split('.')) -2
    if countstepsup < 0:
        countstepsup = 0
    countstepsup += 2

    rd = []
    for v in range(0, countstepsup):
        rd.append("..")
    rd = os.path.join(*rd)
    return rd