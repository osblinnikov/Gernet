import json
import re
import os
from gernetHelpers import *

def importBlocks(a):
    out = ""
    dependenciesList = []
    for v in a.read_data["blocks"]+a.read_data["depends"]:
        dependenciesList.append(v["path"])
    for v in set(dependenciesList):
        out+="\n  s."+getFullName_(v)+" = require(__dirname + \""+os.path.join(*['/../../dist', getFullName_(v), getClassName(v)+'.js'])+"\")"
    if out != "":
        return "if isNode"+out
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

    if a.read_data.get("type")==None or a.read_data["type"]!="buffer":
        if len(a.read_data["blocks"])==0:
            a.classImplements = "Runnable"
        else:
            a.classImplements = "" #GetRunnables
    else:
        a.classImplements = "readerWriterInterface"

    a.defaulRwArguments = [{"name":"grid_id","type":"unsigned"}]
    a.rwArguments = [{"name":"grid_id","type":"unsigned"}]
    if a.read_data.get("rwArgs")!=None:
        a.rwArguments+=a.read_data["rwArgs"]