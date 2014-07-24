import json
import re
import os
from gernetHelpers import *

def importBlocks(a):
    out = []
    dependenciesList = []

    dependenciesList.append(DefaultMapBuffer)

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

    dependenciesList.append(DefaultMapBuffer)

    for v in a.read_data["depends"]:
        dependenciesList.append(v["path"])

    for v in set(dependenciesList):
        out.append("'" + os.path.join('/dist', getFullName_(v), getClassName(v)+'.js') + "'")
    if len(out)>0:
        return "importScripts(\n  " + ",\n  ".join(out) + "\n)"
    return ""

def getFieldsArrStr(a):
    arr = []
    if a.read_data.has_key("props"):
        for i,v in enumerate(a.read_data["props"]):
            t, isObject, isArray, isSerializable = filterTypes_java(v["type"])
            v["type"] = t
            if v.has_key("size"):
                if not isArray:
                    raise Exception("getFieldsArrStr: size of property "+str(i)+" was specified but type is not array!")
                arr.append(v["name"]+" = new Array("+str(v["size"])+")")
            elif isArray:
                raise Exception("getFieldsArrStr: failed because type of property "+str(i)+" is Array but `size` was not specified")
            elif v.has_key("value"):
                if str(v["value"])[0].isdigit() and (str(v["value"]).endswith('L') or str(v["value"]).endswith('f')):
                    v["value"] = str(v["value"])[:-1]
                arr.append(v["name"]+" = "+str(v["value"]))
            else:
                arr.append(v["name"]+" = null")

    return arr


def getargsArrStrs(a):
    arr = []
    for v in a.read_data["args"]:
        t, isObject, isArray, isSerializable = filterTypes_java(v["type"])
        v["type"] = t
        arr.append(v["name"])

    for i,v in enumerate(a.read_data["connection"]["writeTo"]):
        arr.append("w"+str(i))

    for i,v in enumerate(a.read_data["connection"]["readFrom"]):
        arr.append("r"+str(i))

    return arr

def registerConnections(a):
    if len(a.read_data["blocks"]) > 0:
        return ""
    arr = []
    for i,v in enumerate(a.read_data["connection"]["writeTo"]):
        name = str(i)
        if v.has_key("name"):
            name = v["name"]
        arr.append("if w"+name)
        arr.append("  w"+name+".registerSrc(wrk,"+str(i)+")")

    for i,v in enumerate(a.read_data["connection"]["readFrom"]):
        name = str(i)
        if v.has_key("name"):
            name = v["name"]
        arr.append("if r"+name)
        arr.append("  r"+name+".registerDst(wrk,"+str(i)+")")

    return arr

def initializeBuffers(a):
    out = []
    #buffers
    for blockNum, v in enumerate(a.read_data["blocks"]):
        if v.get("type") == None or v["type"] != "buffer":
            continue
        argsList = []
        for d in v["args"]:
            if str(d["value"])[0].isdigit() and (str(d["value"]).endswith('L') or str(d["value"]).endswith('f')):
                d["value"] = str(d["value"])[:-1]
            argsList.append(str(d["value"]))
        #create variables
        out.append(v["name"]+" = new s."+getFullName_(v["path"])+".create("+','.join(argsList)+")")
        #get writer from buffer
        for i,w in enumerate(v["connection"]["writeTo"]):
            #out.append("reader "+v["name"]+"r"+str(i)+" = "+v["name"]+".getReader("+','.join(getRwArgs(i,w))+")")
            connectBufferToReader(a, blockNum, i, w)
        #get reader from buffer
        #for i,w in enumerate(v["connection"]["readFrom"]):
            #out.append("writer "+v["name"]+"w"+str(i)+" = "+v["name"]+".getWriter("+','.join(getRwArgs(i,w))+")")
    return out

def stopKernels(a):
    out = []
    #kernels
    for i,v in enumerate(a.read_data["blocks"]):
        if v.has_key("type") and v["type"] == "buffer":
            continue
        out.append(v["name"]+".onStop()")
    #reverse order
    _out = []
    for i in range(len(out)-1,-1,-1):
        _out.append(out[i])
    return _out

def syncBuffers(a):
    out = []
    #buffers
    for blockNum, v in enumerate(a.read_data["blocks"]):
        if v.get("type") == None or v["type"] != "buffer":
            continue
        #create variables
        out.append(v["name"]+".syncRegister()")
    return out

def initializeKernels(a):
    out = []
    #kernels
    for i,v in enumerate(a.read_data["blocks"]):
        if v.has_key("type") and v["type"] == "buffer":
            continue
        argsList = []
        for d in v["args"]:
            if str(d["value"])[0].isdigit() and (str(d["value"]).endswith('L') or str(d["value"]).endswith('f')):
                d["value"] = str(d["value"])[:-1]
            argsList.append(str(d["value"]))

        out.append(v["name"]+" = new s."+getFullName_(v["path"])+".create("+','.join(argsList+getReadersWriters(a,v,i))+")")
    return out

def getReadersWriters(a,v, curBlock):
    arr = []
    #set writer to the buffer
    for i,w in enumerate(v["connection"]["writeTo"]):
        blockId = w["blockId"]
        if blockId == "export":
            if checkPinId(a.read_data["connection"]["writeTo"], w["pinId"]) != -1:
                arr.append("w"+str(w["pinId"]))
            else:
                raise Exception("pinId w."+str(w["pinId"])+" was not found in the exported connection")
        elif blockId != "internal":
            rblock = a.read_data["blocks"][int(blockId)]
            if rblock["type"] != "buffer":
                raise Exception("Connection from the block allowed only to the block with type='buffer'")
            # r = rblock["connection"]["readFrom"]
            if checkPinId(rblock["connection"]["readFrom"], w["pinId"]) != -1:
                arr.append(rblock["name"])#+"w"+str(w["pinId"])
            else:
                raise Exception("pinId w."+str(w["pinId"])+" was not found in the destination buffer")

    #get reader from buffer
    for i,r in enumerate(v["connection"]["readFrom"]):
        blockId = r["blockId"]
        if blockId == "export":
            if checkPinId(a.read_data["connection"]["readFrom"], r["pinId"]) != -1:
                arr.append("r"+str(r["pinId"]))
            else:
                raise Exception("pinId r."+str(r["pinId"])+" was not found in the exported connection")
        elif blockId != "internal":
            wblock = a.read_data["blocks"][int(blockId)]
            if wblock["type"] != "buffer":
                raise Exception("Connection from the block allowed only to the block with type='buffer'")
            # r = wblock["connection"]["writeTo"]
            if checkPinId(wblock["connection"]["writeTo"], r["pinId"]) != -1:
                arr.append(wblock["name"])#+"r"+str(r["pinId"])
            else:
                raise Exception("pinId r."+str(r["pinId"])+" was not found in the destination buffer")
    return arr


def createWorkerBuffers(a):
    if len(a.read_data["blocks"]) > 0:
        return ""
    arr = []
    lastI = 0
    for i,v in enumerate(a.read_data["connection"]["writeTo"]):
        name = str(i)
        if v.has_key("name"):
            name = v["name"]
        arr.append("bufW"+name+" = new mapBuffer.create()")
        arr.append("bufW"+name+".setDispatcher(" + str(i) +", _this)")
        arr.append("w"+name+" = bufW"+name+".getWriter(onRun)")
        lastI = i

    for i,v in enumerate(a.read_data["connection"]["readFrom"]):
        name = str(i)
        if v.has_key("name"):
            name = v["name"]
        arr.append("bufR"+name+" = new mapBuffer.create()")
        arr.append("bufR"+name+".setDispatcher(" + str(lastI+i) +", _this)")
        arr.append("r"+name+" = bufR"+name+".getReader(onRun)")

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



