import json
import re
import os
from gernetHelpers import *

def importBlocks(a):
    out = []
    dependenciesList = []
    for v in a.read_data["blocks"]+a.read_data["depends"]:
        dependenciesList.append(v["path"])
    for v in set(dependenciesList):
        fname = getFullName_(v)
        cname = getClassName(v)
        out.append("  s."+cname+" = s."+fname+" = require(__dirname + \""+os.path.join(*['/../../dist', fname, cname+'.js'])+"\")")
    if len(out) != 0:
        out.reverse()
        out.append("if isNode")
        out.reverse()
    return out

def importBlocksForTest(a):
    fname = getFullName_(a.read_data["path"])
    cname = getClassName(a.read_data["path"])
    out = importBlocks(a)
    out.append("  s."+cname+" = s."+fname+" = require(__dirname + \""+os.path.join(*['/../../dist', fname, cname+'.js'])+"\")")
    return out

def parsingGernet(a):

    a.read_data = None
    a.read_data = readJson(a.prefix)

    fullName = a.read_data["path"]
    a.version = a.read_data["ver"]
    a.fullName_ = getFullName_(fullName)
    a.className = getClassName(fullName)
    a.companyDomain = getCompanyDomain(fullName)
    a.company = getCompany(fullName)
    a.domainName = getDomainName(fullName)
    a.domainPath = getDomainPath(fullName)

    if not a.read_data.has_key("type") or a.read_data["type"]!="buffer":
        if len(a.read_data["blocks"])==0:
            a.classImplements = "Runnable"
        else:
            a.classImplements = "" #GetRunnables
    else:
        a.classImplements = "readerWriterInterface"

    a.defaulRwArguments = [{"name":"gridId","type":"unsigned"}]
    a.rwArguments = [{"name":"gridId","type":"unsigned"}]
    if a.read_data.has_key("rwArgs"):
        a.rwArguments+=a.read_data["rwArgs"]

def getargsStr(a):
    arr = []
    for v in a.read_data["args"]:
        arr.append(v["name"])

    for i,v in enumerate(a.read_data["connection"]["writeTo"]):
        name = v["name"] if v.has_key("name") else ""
        arr.append("w"+str(i)+name)

    for i,v in enumerate(a.read_data["connection"]["readFrom"]):
        name = v["name"] if v.has_key("name") else ""
        arr.append("r"+str(i)+name)

    return "("+','.join(arr)+")"

def getProps(a):
  arr = []
  if a.read_data.has_key("props"):
    for i,v in enumerate(a.read_data["props"]):
      if v.has_key("size"):
        if not isArray:
          raise Exception("getFieldsArrStr: size of property "+str(i)+" was specified but type is not array!")
        arr.append("that."+v["name"]+" = []")
        arr.append("that."+v["name"]+".length = "+str(v["size"]))
      elif isArray:
        raise Exception("getFieldsArrStr: failed because type of property "+str(i)+" is Array but `size` was not specified")
      elif v.has_key("value"):
        arr.append("that."+v["name"]+" = "+str(v["value"]))
      else:
        arr.append("that."+v["name"])

  for v in a.read_data["args"]:
    arr.append("that."+v["name"]+" = "+v["name"])

  for i,v in enumerate(a.read_data["connection"]["writeTo"]):
    name = v["name"] if v.has_key("name") else ""
    arr.append("that.w"+str(i)+name+" = w"+str(i)+name)

  for i,v in enumerate(a.read_data["connection"]["readFrom"]):
    name = v["name"] if v.has_key("name") else ""
    arr.append("that.r"+str(i)+name+" = r"+str(i)+name)
  return '\n    '.join(arr)