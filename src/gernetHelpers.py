import json
import re
from os.path import join

def readJson(filename):
    json_file_to_read = join(filename)
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