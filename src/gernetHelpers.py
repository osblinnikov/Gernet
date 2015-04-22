import json
import re
import os

#PLEASE change it if you don't want the standard workspace root folder location
PROJECTS_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

DefaultMapBuffer = 'com.github.osblinnikov.cnets.mapBuffer'

def readGernet(filename):
    read_data = readYaml(filename+".yaml")
    if read_data != None:
        read_data['prefix'] = filename+".yaml"
    else:
        read_data = readJson(filename+".json")
        if read_data != None:
            read_data['prefix'] = filename+".json"

    return read_data

def readJson(filename):
    json_file_to_read = os.path.join(filename)
    read_data = None
    try:
        with open (json_file_to_read, "r") as jsonfile:
            print "opened "+json_file_to_read
            pat=re.compile(r'/\*.*?\*/',re.DOTALL|re.M)
            json_data = re.sub(pat, '', jsonfile.read())
            read_data = json.loads(json_data)
            jsonfile.close()
    except:
        # print json_file_to_read+" invalid or not found"
        try:
            jsonfile.close()
        except:
            return read_data

        return read_data

    checkStructure(read_data)
    return read_data


def readYaml(filename):
    file_to_read = os.path.join(filename)
    read_data = None
    try:
        with open (file_to_read, "r") as infile:
            print "opened "+file_to_read
            pat=re.compile(r'/\*.*?\*/',re.DOTALL|re.M)
            read_data = yaml.load(re.sub(pat, '', infile.read()))
            infile.close()
    except:
        # print file_to_read+" invalid or not found"
        try:
            infile.close()
        except:
            return read_data

        return read_data

    checkStructure(read_data)
    return read_data

def checkStructure(read_data):
    if not read_data.has_key("parents"):
        read_data["parents"] = []

    if not read_data.has_key("path"):
        read_data["path"] = ""

    if not read_data.has_key("parallel"):
        read_data["parallel"] = 1

    if not read_data.has_key("topology"):
        read_data["topology"] = []

    for t in read_data["topology"]:
        checkStructure(t)

    if not read_data.has_key("channels"):
        read_data["channels"] = []

    for t in read_data["channels"]:
        checkStructure(t)

    if not read_data.has_key("depends"):
        read_data["depends"] = []

    if not read_data.has_key("props"):
        read_data["props"] = []

    if not read_data.has_key("args"):
        read_data["args"] = []

    if not read_data.has_key("emit"):
        read_data["emit"] = []

    if not read_data.has_key("receive"):
        read_data["receive"] = []

    if not read_data.has_key("hide"):
        read_data["hide"] = False


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
    if t in ["byte"]:
        t = "byte" if isArray else "byte"
        isObject = False
        serializableType = True
    if t in ["char"]:
        t = "char" if isArray else "char"
        isObject = False
        serializableType = True
    if t in ["int"]:
        t = "int" if isArray else "int"
        isObject = False
        serializableType = True
    if t in ["unsigned","long"]:
        t = "long" if isArray else "long"
        isObject = False
        serializableType = True
    if t in ["boolean"]:
        t = "boolean" if isArray else "boolean"
        isObject = False
        serializableType = True
    if t in ["double"]:
        t = "double" if isArray else "double"
        isObject = False
        serializableType = True
    if t in ["float"]:
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
    if t in ["string","char*"]:
        t = "char*"
        serializableType = True
    if t in ["char"]:
        t = "char"
        isObject = False
        serializableType = True
    if t in ["int"]:
        t = "int32_t"
        isObject = False
        serializableType = True
    if t in ["unsigned"]:
        t = "uint32_t"
        isObject = False
        serializableType = True
    if t  in ["long"]:
        t = "int64_t"
        isObject = False
        serializableType = True
    if t in ["boolean"]:
        t = "BOOL" if isArray else "BOOL"
        isObject = False
        serializableType = True
    if t in ["double"]:
        t = "double"
        isObject = False
        serializableType = True
    if t in ["float"]:
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