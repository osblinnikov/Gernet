import json
import re
from gernetHelpers import *

def getReaderWriterArgumentsStrArr(readerWriterArguments):
  readerWriterArgumentsStrArr = []
  if readerWriterArguments[0]["name"] != "grid_id":
    raise Exception("getReaderWriterArgumentsStrArr: readerWriterArguments[0][\"name\"]!=\"grid_id\"")
  for value in readerWriterArguments:
    if value["type"] == "unsigned":
      value["type"] = "long"
    readerWriterArgumentsStrArr.append(value["type"]+" "+value["name"])
  return readerWriterArgumentsStrArr

def getReaderWriterArgumentsStrarrDel0(readerWriterArguments):
  readerWriterArgumentsStrArr = getReaderWriterArgumentsStrArr(readerWriterArguments)
  del readerWriterArgumentsStrArr[0]
  return readerWriterArgumentsStrArr

def getReaderWriterArgumentsStr(readerWriterArguments):
  return ','.join(getReaderWriterArgumentsStrArr(readerWriterArguments))

def getFieldsArrStr(a):
  arr = []
  props = []
  if a.read_data.has_key("props"):
    for i,v in enumerate(a.read_data["props"]):
      t, isObject, isArray, isSerializable = filterTypes_java(v["type"])
      v["type"] = t
      if v.has_key("size"):
        if not isArray:
          raise Exception("getFieldsArrStr: size of property "+str(i)+" was specified but type is not array!")
        arr.append(t+" "+v["name"])
      elif isArray:
        raise Exception("getFieldsArrStr: failed because type of property "+str(i)+" is Array but `size` was not specified")
      elif v.has_key("value"):
        arr.append(t+" "+v["name"]+" = "+str(v["value"]))
      else:
        arr.append(t+" "+v["name"])

  for v in a.read_data["args"]:
    t, isObject, isArray, isSerializable = filterTypes_java(v["type"])
    v["type"] = t
    arr.append(v["type"]+" "+v["name"])

  for i,v in enumerate(a.read_data["connection"]["writeTo"]):
    arr.append("writer w"+str(i))

  for i,v in enumerate(a.read_data["connection"]["readFrom"]):
    arr.append("reader r"+str(i))

  noSelectors = False
  if a.read_data["connection"].has_key("noSelectors"):
      noSelectors = a.read_data["connection"]["noSelectors"]
  if len(a.read_data["connection"]["readFrom"]) > 1 and not noSelectors:
    arr.append("reader rSelect")
    arr.append("selector readersSelector")
  return arr

def getargsArrStrs(a):
  arr = []
  for v in a.read_data["args"]:
    t, isObject, isArray, isSerializable = filterTypes_java(v["type"])
    v["type"] = t
    arr.append(t+" "+v["name"])

  for i,v in enumerate(a.read_data["connection"]["writeTo"]):
    arr.append("writer w"+str(i))

  for i,v in enumerate(a.read_data["connection"]["readFrom"]):
    arr.append("reader r"+str(i))

  return arr

def groupId(path):
  path = path.split(".")
  del path[-1]
  return '.'.join(path)
def artifactId(path):
  path = path.split(".")
  return path[-1]

def parsingGernet(a):

  a.read_data = None
  a.read_data = readJson(a.prefix)

  fullName = a.read_data["path"]
  a.version = a.read_data["ver"]
  fullNameList = fullName.split('.')
  a.fullName_ = '_'.join(fullNameList)
  a.className = fullNameList[-1]
  a.companyDomain = fullNameList[1]+'.'+fullNameList[0]
  a.company = fullNameList[1]

  del fullNameList[-1]
  a.domainName = '.'.join(fullNameList)

  fullNameList = fullName.split('.')
  to_delete = [0,1]
  for offset, index in enumerate(to_delete):
    index -= offset
    del fullNameList[index]
  a.domainPath = a.companyDomain+'/'+('/'.join(fullNameList))

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
  a.arrDel0 = getReaderWriterArgumentsStrarrDel0(a.rwArguments)
  a.rwArgumentsStr = getReaderWriterArgumentsStr(a.rwArguments)

def getProps(a):
  fieldsArray = getFieldsArrStr(a)
  out = "  "+';'.join(fieldsArray)+';\n' if len(fieldsArray)>0 else ''
  return out

def getConstructor(a):
  out = ""
  argsArray = getargsArrStrs(a)
  out += "  public "+a.className+"("+','.join(argsArray)+"){"
  for value in a.read_data["args"]:
    out += "\n    this."+value["name"]+" = "+value["name"]+";"
  for i,v in enumerate(a.read_data["connection"]["writeTo"]):
    out += "\n    this.w"+str(i)+" = w"+str(i)+";"
  for i,v in enumerate(a.read_data["connection"]["readFrom"]):
    out += "\n    this.r"+str(i)+" = r"+str(i)+";"

  if a.read_data.has_key("props"):
    for i,v in enumerate(a.read_data["props"]):
      if v.has_key("value"):
        out += "\n    this."+v["name"]+" = "+str(v["value"])+";"
      elif v.has_key("size"):
        out += "\n    this."+v["name"]+" = new "+v["type"][:-2]+"["+str(v["size"])+"];"

  selectableArgs = []
  for i,v in enumerate(a.read_data["args"]):
    if v.has_key("selectable") and v["selectable"] == True:
      if v["type"] != 'reader[]':
        raise Exception("every selectable argument should have reader[] type, but we have "+v["type"]+" "+v["name"])
      selectableArgs.append(v)

  noSelectors = False
  if a.read_data["connection"].has_key("noSelectors"):
      noSelectors = a.read_data["connection"]["noSelectors"]

  if not noSelectors and (len(a.read_data["connection"]["readFrom"]) > 1 or len(selectableArgs)>0):
    selectablesCount = str(len(a.read_data["connection"]["readFrom"]))
    for i,v in enumerate(selectableArgs):
      selectablesCount += " + "+str(v["name"])+".length"
    out += "\n    reader[] arrReaders = new reader["+selectablesCount+"];"

    lastId = 0
    for i,v in enumerate(a.read_data["connection"]["readFrom"]):
      out += "\n    arrReaders["+str(i)+"] = r"+str(i)+";"
      lastId = i
    if len(selectableArgs)>0:
      out += "\n    int totalLength = "+str(lastId + 1)+";"
      for i,v in enumerate(selectableArgs):
        out += "\n    for(int i=0;i<"+str(v["name"])+".length; i++){"
        out += "\n      arrReaders[totalLength + i] = "+v["name"]+"[i];"
        out += "\n    }"
        if i+1 != len(selectableArgs):
          out += "\n    totalLength += "+str(v["name"])+".length;"
    out += "\n    this.readersSelector = new selector(arrReaders);"
    out += "\n    this.rSelect = readersSelector.getReader(0,-1);"
  out += "\n    onCreate();"
  out += "\n    initialize();"
  out += "\n  }"
  return out

def getContainerClass(a):
  out = ""
  if len(a.arrDel0)>0:
    out += "\nclass "+a.className+"Container{"
    for rwArg in a.arrDel0:
      out += "\n  "+rwArg+";"
    out += "\n}"
  return out

def getReaderWriter(a):
  out = ""
  out += "\npublic reader getReader("+a.rwArgumentsStr+"){"
  out += "\n  Object container = null;"
  if len(a.rwArguments) == 0:
    raise Exception("len(a.rwArguments) == 0")
  elif len(a.rwArguments) > 1:
    out += "\n  "+a.className+"Container obj = new "+a.className+"Container();"
    for value in a.rwArguments:
      if value['name'] != "grid_id":
        out += "\n  obj."+value['name']+" = "+value["name"]+";"
    out += "\n  container = obj;"
  out += "\n  return new reader(new bufferKernelParams(this, "+a.rwArguments[0]["name"]+", container));"
  out += "\n}"

  out += "\npublic writer getWriter("+a.rwArgumentsStr+"){"
  out += "\n  Object container = null;"
  if len(a.rwArguments) == 0:
    raise Exception("len(a.rwArguments) == 0")
  elif len(a.rwArguments) > 1:
    out += "\n  "+a.className+"Container obj = new "+a.className+"Container();"
    for value in a.rwArguments:
      if value['name'] != "grid_id":
        out += "\n  obj."+value['name']+" = "+value["name"]+";"
    out += "\n  container = obj;"
  out += "\n  return new writer(new bufferKernelParams(this, "+a.rwArguments[0]["name"]+", container));"
  out += "\n}"
  return out

def importBlocks(a):
    out = ""
    dependenciesList = []
    for v in a.read_data["blocks"]+a.read_data["depends"]:
        dependenciesList.append(v["path"])
    for v in set(dependenciesList):
        out+="\nimport "+v+".*;"
    return out

def declareBlocks(a):
  out = ""
  for v in a.read_data["blocks"]:
    pathList = v["path"].split('.')
    out += v["path"]+"."+pathList[-1]+" "+v["name"]+";"
  return out

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
    
def getReadersWriters(a,v, curBlock):
  arr = []
  #set writer to the buffer
  for i,w in enumerate(v["connection"]["writeTo"]):
    blockId = w["blockId"]
    if blockId == "export":
      if checkPinId(a.read_data["connection"]["writeTo"], w["pinId"]) != -1:
        arr.append("this.w"+str(w["pinId"]))
      else:
        raise Exception("pinId this.w."+str(w["pinId"])+" was not found in the exported connection")
    elif blockId != "internal":
      rblock = a.read_data["blocks"][int(blockId)]
      if rblock["type"] != "buffer":
        raise Exception("Connection from the block allowed only to the block with type='buffer'")
      # r = rblock["connection"]["readFrom"]
      if checkPinId(rblock["connection"]["readFrom"], w["pinId"]) != -1:
        arr.append(rblock["name"]+"w"+str(w["pinId"]))
      else:
        raise Exception("pinId w."+str(w["pinId"])+" was not found in the destination buffer")

  #get reader from buffer
  for i,r in enumerate(v["connection"]["readFrom"]):
    blockId = r["blockId"]
    if blockId == "export":
      if checkPinId(a.read_data["connection"]["readFrom"], r["pinId"]) != -1:
        arr.append("this.r"+str(r["pinId"]))
      else:
        raise Exception("pinId this.r."+str(r["pinId"])+" was not found in the exported connection")
    elif blockId != "internal":
      wblock = a.read_data["blocks"][int(blockId)]
      if wblock["type"] != "buffer":
        raise Exception("Connection from the block allowed only to the block with type='buffer'")
      # r = wblock["connection"]["writeTo"]
      if checkPinId(wblock["connection"]["writeTo"], r["pinId"]) != -1:
        arr.append(wblock["name"]+"r"+str(r["pinId"]))
      else:
        raise Exception("pinId r."+str(r["pinId"])+" was not found in the destination buffer")
  return arr

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

def initializeKernels(a):
  out = ""
  #kernels
  for i,v in enumerate(a.read_data["blocks"]):
    if v.has_key("type") and v["type"] == "buffer":
      continue
    pathList = v["path"].split('.')
    argsList = []
    for d in v["args"]:
      castType = ""
      if d.has_key("type"):
        castType = "("+d["type"]+")"
      argsList.append(castType+str(d["value"]))

    out += "\n    "+v["name"]+" = new "+v["path"]+"."+pathList[-1]+"("+','.join(argsList+getReadersWriters(a,v,i))+");"

  return out

def runBlocks(a):
  out = ""
  #kernels
  for i,v in enumerate(a.read_data["blocks"]):
    if v.has_key("type") and v["type"] == "buffer":
      continue
    out += "\n    "+v["name"]+".run();"
  return out

# def stopBlocks(a):
#   out = ""
#   #kernels
#   for i,v in enumerate(a.read_data["blocks"]):
#     if v.has_key("type") and v["type"] == "buffer":
#       continue
#     out += "\n    "+v["name"]+".stop();"
#   return out

def getDefaultRunParameters(a):
  argsList = []
  for v in a.read_data["args"]:
    t, isObject, isArray, isSerializable = filterTypes_java(v["type"])
    if v.has_key("value_java"):
      argsList.append(str(v["value_java"]))
    elif v.has_key("value"):
      argsList.append(str(v["value"]))
    elif isArray:
      t = t[:-2]
      argsList.append("new "+t+"[1]")
    elif isObject:
      argsList.append("null")
    else:
      argsList.append("0")
  for v in a.read_data["connection"]["writeTo"]:
    argsList.append("null")
  for v in a.read_data["connection"]["readFrom"]:
    argsList.append("null")
  return ','.join(argsList)

def startRunnables(a):
  typeOfBlock = "kernel"
  if a.read_data.has_key("type"):
    typeOfBlock = a.read_data["type"]

  out = a.className+" classObj = new "+a.className+"("+getDefaultRunParameters(a)+");"
  if typeOfBlock == "kernel":
    out += '''
    runnablesContainer runnables = classObj.getRunnables();
    runnables.launch(true);
    '''
  return out

def testRunnables(a):
  typeOfBlock = "kernel"
  if a.read_data.has_key("type"):
    typeOfBlock = a.read_data["type"]

  out = a.className+" classObj = new "+a.className+"("+getDefaultRunParameters(a)+");"
  if typeOfBlock == "kernel":
    out += '''
    runnablesContainer runnables = classObj.getRunnables();
    runnables.launch(false);
    runnables.stop();
    '''
  return out

def getRunnables(a):
  sizeRunnables = 0
  out = ""

  for blockNum, v in enumerate(a.read_data["blocks"]):
    if v.has_key("type") and v["type"] == "buffer":
      continue
    out += "    arrContainers["+str(sizeRunnables)+"] = "+v["name"]+".getRunnables();\n"
    sizeRunnables += 1

  if sizeRunnables == 0:
    return '''
    runnablesContainer runnables = new runnablesContainer();
    runnables.setCore(this);
    return runnables;'''
  else:
    return  '''
    runnablesContainer runnables = new runnablesContainer();
    runnablesContainer[] arrContainers = new runnablesContainer['''+str(sizeRunnables)+"];\n"+out+'''
    runnables.setContainers(arrContainers);
    return runnables;'''