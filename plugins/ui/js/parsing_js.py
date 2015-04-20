import json
import re
import os
from gernetHelpers import *

def importBlocks(a):
    out = []
    dependenciesList = []
    for v in a.read_data["topology"]+a.read_data["depends"]:
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

def rootRelativePath(a):
    return getRootPath(a.read_data["path"])

def parsingGernet(a):

    a.read_data = None
    a.read_data = readJson(a.prefix)

    fullName = a.read_data["path"]
    # a.version = a.read_data["ver"]
    a.fullName_ = getFullName_(fullName)
    a.className = getClassName(fullName)
    a.companyDomain = getCompanyDomain(fullName)
    a.company = getCompany(fullName)
    a.domainName = getDomainName(fullName)
    a.domainPath = getDomainPath(fullName)

    if not a.read_data.has_key("type") or a.read_data["type"]!="buffer":
        if len(a.read_data["topology"])==0:
            a.classImplements = "Runnable"
        else:
            a.classImplements = "" #GetRunnables
    else:
        a.classImplements = "readerWriterInterface"

    a.defaulRwArguments = [{"name":"gridId","type":"unsigned"}]
    a.rwArguments = [{"name":"gridId","type":"unsigned"}]
    if a.read_data.has_key("rwArgs"):
        a.rwArguments+=a.read_data["rwArgs"]