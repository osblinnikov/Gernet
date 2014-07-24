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
        fname = getFullName_(v)
        cname = getClassName(v)
        out+="\n  s."+cname+" = s."+fname+" = require(__dirname + \""+os.path.join(*['/../../dist', fname, cname+'.js'])+"\")"
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

def importScripts(a):
    if len(a.read_data["blocks"]) > 0:
        return ""
    out = []
    dependenciesList = []
    for v in a.read_data["depends"]:
        dependenciesList.append(v["path"])
    for v in set(dependenciesList):
        out.append("'" + os.path.join('/dist', getFullName_(v), getClassName(v)+'.js') + "'")
    if len(out)>0:
        return "importScripts(\n  " + ",\n  ".join(out) + "\n)"
    return ""

def createWorkerBuffers(a):
    if len(a.read_data["blocks"]) > 0:
        return ""
    arr = []
    lastI = 0
    for i,v in enumerate(a.read_data["connection"]["writeTo"]):
        name = str(i)
        if v.has_key("name"):
            name = v["name"]
        arr.append("w"+name+" = (new mapBuffer.create(" + str(i) +", _this)).getWriter(onRun)")
        lastI = i

    for i,v in enumerate(a.read_data["connection"]["readFrom"]):
        name = str(i)
        if v.has_key("name"):
            name = v["name"]
        arr.append("r"+name+" = (new mapBuffer.create(" + str(lastI+i) +", _this)).getReader(onRun)")

    return "\n".join(arr)

def checkPinId(arrPins, pinId):
    for i,pin in enumerate(arrPins):
        if pin.get("grid_id"):
            grid_id = pin["grid_id"]
            if grid_id == pinId:
                return i
    if len(arrPins)>pinId:
        return pinId
    else:
        return -1

def getRwArgs(i,w):
    grid_id = i
    if w.get("grid_id"):
        grid_id = w["grid_id"]
    rwArgs = []
    if w.has_key("rwArgs"):
        for arg in w["rwArgs"]:
            if arg.get("value") == None:
                raise Exception("rwArgs is specified but `value` field was not set")
            rwArgs.append(str(arg["value"]))
    return [str(grid_id)]+rwArgs

def connectBufferToReader(a, blockNum, i, w):
    blockId = w["blockId"]
    if blockId == "export":
        raise Exception("Export readerWriter from buffer is forbidden! only kernels can do it [block id = "+str(blockNum)+"]")
    elif blockId != "internal":
        wblock = a.read_data["blocks"][int(blockId)]
        if wblock.has_key("type") and wblock["type"] == "buffer":
            raise Exception("Interconnections of buffers ["+str(blockNum)+" and "+str(blockId)+"] are forbidden")
        arr_id = checkPinId(wblock["connection"]["readFrom"],w["pinId"])
        if arr_id == -1:
            raise Exception("pinId w."+str(w["pinId"])+" was not found in the destination buffer")
        if w["pinId"] != arr_id:
            raise Exception("wrong parameter grid_id!=pinId in the block "+str(blockNum)+", pin "+str(i))

        pinObject = wblock["connection"]["readFrom"][arr_id]
        if pinObject.has_key("blockId") and pinObject.has_key("pinId") and pinObject["blockId"] != "export":
            if int(pinObject["blockId"])!=blockNum or int(pinObject["pinId"])!=i:
                raise Exception("Connection of block "+str(blockNum)+", pin "+str(i)+" with "+str(blockId)+", pin "+str(w["pinId"])+" failed because the last already connected to "+str(pinObject["blockId"])+", "+str(pinObject["pinId"]))
        pinObject.update({"blockId":blockNum})
        pinObject.update({"pinId":i})

def initializeBuffers(a):
    out = ""
    #buffers
    for blockNum, v in enumerate(a.read_data["blocks"]):
        if v.get("type") == None or v["type"] != "buffer":
            continue
        pathList = v["path"].split('.')
        argsList = []
        for d in v["args"]:
            castType = ""
            if d.has_key("type"):
                castType = "("+d["type"]+")"
            argsList.append(castType+str(d["value"]))
        #create variables
        out += "\n    "+v["name"]+" = new "+v["path"]+"."+pathList[-1]+"("+','.join(argsList)+");"
        #get writer from buffer
        for i,w in enumerate(v["connection"]["writeTo"]):
            out += "\n    reader "+v["name"]+"r"+str(i)+" = "+v["name"]+".getReader("+','.join(getRwArgs(i,w))+");"
            connectBufferToReader(a, blockNum, i, w)
        #get reader from buffer
        for i,w in enumerate(v["connection"]["readFrom"]):
            out += "\n    writer "+v["name"]+"w"+str(i)+" = "+v["name"]+".getWriter("+','.join(getRwArgs(i,w))+");"
    return out

