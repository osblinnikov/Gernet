import json
import re
from gernetHelpers import *

def getReaderWriterArgumentsStrArr(readerWriterArguments):
  readerWriterArgumentsStrArr = []
  if readerWriterArguments[0]["name"] != "gridId":
    raise Exception("getReaderWriterArgumentsStrArr: readerWriterArguments[0][\"name\"]!=\"gridId\"")
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

  for i,v in enumerate(a.read_data["emit"]):
    arr.append("writer w"+str(i))

  for i,v in enumerate(a.read_data["receive"]):
    arr.append("reader r"+str(i))

  noSelectors = False
  if a.read_data.has_key("noSelectors"):
      noSelectors = a.read_data["noSelectors"]
  if len(a.read_data["receive"]) > 1 and not noSelectors:
    arr.append("reader rSelect")
    arr.append("selector readersSelector")
  return arr

def getargsArrStrs(a):
  arr = []
  for v in a.read_data["args"]:
    t, isObject, isArray, isSerializable = filterTypes_java(v["type"])
    v["type"] = t
    arr.append(t+" "+v["name"])

  for i,v in enumerate(a.read_data["emit"]):
    arr.append("writer w"+str(i))

  for i,v in enumerate(a.read_data["receive"]):
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

  fullName = a.read_data["name"]
  # a.version = a.read_data["ver"]
  fullNameList = fullName.split('.')
  a.fullName_ = '_'.join(fullNameList)
  a.className = fullNameList[-1]
  a.targetClassName = ".".join(fullNameList[:-1])
  a.targetClassName = ".".join([a.targetClassName]+[fullNameList[-2]])
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
  for i,v in enumerate(a.read_data["emit"]):
    out += "\n    this.w"+str(i)+" = w"+str(i)+";"
  for i,v in enumerate(a.read_data["receive"]):
    out += "\n    this.r"+str(i)+" = r"+str(i)+";"

  if a.read_data.has_key("props"):
    for i,v in enumerate(a.read_data["props"]):
      if v.has_key("value"):
        out += "\n    this."+v["name"]+" = "+str(v["value"])+";"
      elif v.has_key("size"):
        out += "\n    this."+v["name"]+" = new "+v["type"][:-2]+"["+str(v["size"])+"];"
        t, isObject, isArray, isSerializable = filterTypes_java(v["type"])
        if isArray:
          _t, isObject, _isArray, _isSerializable = filterTypes_java(v["type"][:-2])
        if isObject and (not v.has_key("init") or v["init"]==True):
            out += "\n    for(int j=0;j<this."+v["name"]+".length;j++){"
            out += "\n      this."+v["name"]+"[j] = new "+v["type"][:-2]+"();"
            out += "\n    }"


  selectableArgs = []
  for i,v in enumerate(a.read_data["args"]):
    if v.has_key("selectable") and v["selectable"] == True:
      if v["type"] != 'reader[]':
        raise Exception("every selectable argument should have reader[] type, but we have "+v["type"]+" "+v["name"])
      selectableArgs.append(v)

  noSelectors = False
  if a.read_data.has_key("noSelectors"):
    noSelectors = a.read_data["noSelectors"]

  if not noSelectors and (len(a.read_data["receive"]) > 1 or len(selectableArgs)>0):
    selectablesCount = str(len(a.read_data["receive"]))
    for i,v in enumerate(selectableArgs):
      selectablesCount += " + "+str(v["name"])+".length"
    out += "\n    reader[] arrReaders = new reader["+selectablesCount+"];"

    lastId = 0
    for i,v in enumerate(a.read_data["receive"]):
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
      if value['name'] != "gridId":
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
      if value['name'] != "gridId":
        out += "\n  obj."+value['name']+" = "+value["name"]+";"
    out += "\n  container = obj;"
  out += "\n  return new writer(new bufferKernelParams(this, "+a.rwArguments[0]["name"]+", container));"
  out += "\n}"
  return out

def importBlocks(a):
  out = ""
  dependenciesList = []
  for v in a.read_data["topology"]+a.read_data["depends"]:
    dependenciesList.append(v["path"])
  for v in set(dependenciesList):
    out+="\nimport "+v+".*;"
  return out

def declareBlocks(a):
  out = ""
  for v in a.read_data["topology"]:
    pathList = v["path"].split('.')
    out += v["path"]+"."+pathList[-1]+" "+v["name"]
    if v.has_key("parallel"):
      out += "[]"
    out += ";"
  return out

def checkPinId(arrPins, pinId):
  for i,pin in enumerate(arrPins):
    if pin.has_key("gridId"):
      gridId = pin["gridId"]
      if gridId == pinId:
        if pin.has_key("is_busy"):
          print arrPins[pinId]
          return -1
        pin["is_busy"] = True
        return i
  if len(arrPins)>pinId:
    pin = arrPins[pinId]
    if pin.has_key("is_busy"):
      print arrPins[pinId]
      return -1
    pin["is_busy"] = True
    return pinId
  else:
    print "len(arrPins)>pinId : "+str(len(arrPins))+">"+str(pinId)
    return -1
    
def getReadersWriters(a,v, makeCopies):
  arr = []
  #set writer to the buffer
  for i,w in enumerate(v["emit"]):
    blockId = w["blockId"]
    if blockId == "export":
      if checkPinId(a.read_data["emit"], w["pinId"]) != -1:
        arr.append("this.w"+str(w["pinId"]))
      else:
        raise Exception("pinId this.w"+str(w["pinId"])+" was not found in the exported connection")
    elif blockId != "internal":
      rblock = a.read_data["topology"][int(blockId)]
      if not rblock.has_key("type") or rblock["type"] != "buffer":
        raise Exception("Connection from the block allowed only to the block with type='buffer'")
      # r = rblock["receive"]
      if checkPinId(rblock["receive"], w["pinId"]) != -1:
        arr.append(rblock["name"]+"w"+str(w["pinId"]))
      else:
        raise Exception("pinId w"+str(w["pinId"])+" was not found in the destination buffer "+str(blockId))

  #get reader from buffer
  for i,r in enumerate(v["receive"]):
    blockId = r["blockId"]
    if blockId == "export":
      if checkPinId(a.read_data["receive"], r["pinId"]) != -1:
        arr.append("this.r"+str(r["pinId"]))
      else:
        raise Exception("pinId this.r"+str(r["pinId"])+" was not found in the exported connection")
    elif blockId != "internal":
      wblock = a.read_data["topology"][int(blockId)]
      if wblock["type"] != "buffer":
        raise Exception("Connection from the block allowed only to the block with type='buffer'")
      # r = wblock["emit"]
      if checkPinId(wblock["emit"], r["pinId"]) != -1:
        arr.append(wblock["name"]+"r"+str(r["pinId"]))
      else:
        raise Exception("pinId r"+str(r["pinId"])+" was not found in the destination buffer "+str(blockId))
  if makeCopies:
      for i,r in enumerate(arr):
          arr[i] = r+".copy()"
  return arr

def connectBufferToReader(a, blockNum, i, w):
  blockId = w["blockId"]
  if blockId == "export":
    raise Exception("Export readerWriter from buffer is forbidden! only kernels can do it [block id = "+str(blockNum)+"]")
  elif blockId != "internal":
    wblock = a.read_data["topology"][int(blockId)]
    if wblock.has_key("type") and wblock["type"] == "buffer":
      raise Exception("Interconnections of buffers ["+str(blockNum)+" and "+str(blockId)+"] are forbidden")
    arr_id = checkPinId(wblock["receive"],w["pinId"])
    if arr_id == -1:
      # print wblock["receive"]
      raise Exception("pinId w"+str(w["pinId"])+" was not found in the destination buffer "+str(blockId))
    if w["pinId"] != arr_id:
      raise Exception("wrong parameter gridId!=pinId in the block "+str(blockNum)+", pin "+str(i))

    pinObject = wblock["receive"][arr_id]
    if pinObject.has_key("blockId") and pinObject.has_key("pinId") and pinObject["blockId"] != "export":
      if int(pinObject["blockId"])!=blockNum or int(pinObject["pinId"])!=i:
        raise Exception("Connection of block "+str(blockNum)+", pin "+str(i)+" with "+str(blockId)+", pin "+str(w["pinId"])+" failed because the last already connected to "+str(pinObject["blockId"])+", "+str(pinObject["pinId"]))
    pinObject.update({"blockId":blockNum})
    pinObject.update({"pinId":i})

def getRwArgs(i,w):
  gridId = i
  if w.has_key("gridId"):
    gridId = w["gridId"]
  rwArgs = []
  if w.has_key("rwArgs"):
    for arg in w["rwArgs"]:
      if not arg.has_key("value"):
        raise Exception("rwArgs is specified but `value` field was not set")
      rwArgs.append(str(arg["value"]))
  return [str(gridId)]+rwArgs

def initializeBuffers(a):
  out = ""
  #buffers
  for blockNum, v in enumerate(a.read_data["topology"]):
    if not v.has_key("type") or v["type"] != "buffer":
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
    for i,w in enumerate(v["emit"]):
      out += "\n    reader "+v["name"]+"r"+str(i)+" = "+v["name"]+".getReader("+','.join(getRwArgs(i,w))+");"
      connectBufferToReader(a, blockNum, i, w)
    #get reader from buffer
    for i,w in enumerate(v["receive"]):
      out += "\n    writer "+v["name"]+"w"+str(i)+" = "+v["name"]+".getWriter("+','.join(getRwArgs(i,w))+");"
  return out

def initializeKernels(a):
  out = ""
  #kernels
  for i,v in enumerate(a.read_data["topology"]):
    if v.has_key("type") and v["type"] == "buffer":
      continue
    pathList = v["path"].split('.')
    argsList = []
    for d in v["args"]:
      castType = ""
      if d.has_key("type"):
        castType = "("+d["type"]+")"
      argsList.append(castType+str(d["value"]))

    if v.has_key("parallel"):
        out += "\n    "+v["name"]+" = new "+v["path"]+"."+pathList[-1]+"["+str(v["parallel"])+"];"
        out += "\n    for(int j=0;j<"+str(v["parallel"])+";j++){"
        out += "\n      "+v["name"]+"[j] = new "+v["path"]+"."+pathList[-1]+"("+','.join(argsList+getReadersWriters(a,v,True))+");"
        out += "\n    }"
    else:
        out += "\n    "+v["name"]+" = new "+v["path"]+"."+pathList[-1]+"("+','.join(argsList+getReadersWriters(a,v,False))+");"

  return out

def runBlocks(a):
  out = ""
  #kernels
  for i,v in enumerate(a.read_data["topology"]):
    if v.has_key("type") and v["type"] == "buffer":
      continue
    out += "\n    "+v["name"]+".run();"
  return out

# def stopBlocks(a):
#   out = ""
#   #kernels
#   for i,v in enumerate(a.read_data["topology"]):
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
  for v in a.read_data["emit"]:
    argsList.append("null")
  for v in a.read_data["receive"]:
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

def evalSize(sizeRunnables):
    try:
        evaluated = str(eval(sizeRunnables))
    except:
        evaluated = sizeRunnables
    return evaluated

def getRunnables(a):
  sizeRunnables = "0"
  out = ""

  for blockNum, v in enumerate(a.read_data["topology"]):
    if v.has_key("type") and v["type"] == "buffer":
      continue
    if v.has_key("parallel"):
        out += "    for(int j=0;j<"+str(v["parallel"])+";j++){\n"
        out += "      arrContainers["+str(evalSize(sizeRunnables))+"+j] = "+v["name"]+"[j].getRunnables();\n"
        out += "    }\n"
        sizeRunnables += "+"+str(v["parallel"])
    else:

        out += "    arrContainers["+str(evalSize(sizeRunnables))+"] = "+v["name"]+".getRunnables();\n"
        sizeRunnables += "+1"


  if sizeRunnables == "0":
    return '''
    runnablesContainer runnables = new runnablesContainer();
    runnables.setCore(this);
    return runnables;'''
  else:
    return  '''
    runnablesContainer runnables = new runnablesContainer();
    runnablesContainer[] arrContainers = new runnablesContainer['''+str(evalSize(sizeRunnables))+"];\n"+out+'''
    runnables.setContainers(arrContainers);
    return runnables;'''

def serializeWith(a, serializerPostfix):
    out = ""
    for v in a.read_data["props"]+a.read_data["args"]:
        t, isObject, isArray, serializableType = filterTypes_java(v["type"])
        if isArray:
            t = t[:-2]
        if serializableType:
            if len(v["type"])>2 and isArray:
                out += '''
      if (!s.serializeValue((int)that.'''+v["name"]+'''.length)) { return false; }
      for(int i=0; i<that.'''+v["name"]+'''.length; i++) {
        if (!s.serializeValue(that.'''+v["name"]+'''[i])) { return false; }
      }'''
            else:
                out += '''
      if(!s.serializeValue(that.'''+v["name"]+''')){ return false; }'''
        else:
            tPrefix = ".".join((t.split(".")[:-1]))
            if len(v["type"])>2 and isArray:
                out += '''
      if (!s.serializeValue((int)that.'''+v["name"]+'''.length)) { return false; }
      for(int i=0; i<that.'''+v["name"]+'''.length; i++) {
        if (!(new '''+tPrefix+serializerPostfix+"()).serializeWith(s,that."+v["name"]+'''[i])) { return false;}
      }'''
            else:
                out += '''
      if (!(new '''+tPrefix+serializerPostfix+"()).serializeWith(s,that."+v["name"]+''')) { return false;}'''
    return out

def deserializeWith(a, deserializerPostfix):
    out = ""
    for v in a.read_data["props"]+a.read_data["args"]:
        t, isObject, isArray, serializableType = filterTypes_java(v["type"])
        if isArray:
            t = t[:-2]
        if serializableType:
            if len(v["type"])>2 and isArray:
                out += '''
      that.'''+v["name"]+''' = new '''+t+'''[d.deserializeValue(int.class)];
      for(int i=0; i<that.'''+v["name"]+'''.length; i++) {
        that.'''+v["name"]+'''[i] = d.deserializeValue('''+t+'''.class);
      }'''
            else:
                out += '''
      that.'''+v["name"]+''' = d.deserializeValue('''+t+'''.class);'''
        else:
            tPrefix = ".".join((t.split(".")[:-1]))
            if len(v["type"])>2 and isArray:
                out += '''
      that.'''+v["name"]+''' = new '''+t+'''[d.deserializeValue(int.class)];
      for(int i=0; i<that.'''+v["name"]+'''.length; i++) {
        that.'''+v["name"]+'''[i] = new '''+t+'''();
        if (!(new '''+tPrefix+deserializerPostfix+"()).deserializeWith(d,that."+v["name"]+'''[i])) { return false;}
      }'''
            else:
                out+= '''
      if (!(new '''+tPrefix+deserializerPostfix+"()).deserializeWith(d,that."+v["name"]+''')) { return false;}'''

    return out


def fillConnectorsNames(a):
    if a.read_data.has_key("serializatorPath"):
      serializatorPath = a.read_data["serializatorPath"]
    else:
      serializatorPath = "com.github.osblinnikov.cnetsTransports.msgpack.msgPackSerializer"

    if a.read_data.has_key("deserializatorPath"):
      deserializatorPath = a.read_data["deserializatorPath"]
    else:
      deserializatorPath = "com.github.osblinnikov.cnetsTransports.msgpack.msgPackDeserializer"

    if a.read_data.has_key("serializePackagePostfix"):
      serializePackagePostfix = a.read_data["serializePackagePostfix"]
    else:
      serializePackagePostfix = ".msgpack.msgpack"

    out = ["/* +1 everywhere for repo receivers and senders*/"]
    if len(a.read_data["emit"]) - 1 > 0:
        out.append("subscribedBuffersNames = new String["+str(len(a.read_data["emit"]) - 1 + 1)+"]"+";")
        out.append("allWriters = new writer["+str(len(a.read_data["emit"]) - 1 + 1)+"]"+";")
        out.append("allWriters_callbacks = new deserializeStreamCallback["+str(len(a.read_data["emit"]) - 1 + 1)+"]"+";")
        out.append("subscribedBuffersNames[0] = \"nodeRepository\";")
        out.append("allWriters_callbacks[0] = new "+deserializatorPath+"(new com.github.osblinnikov.cnetsTransports.nodeRepositoryProtocol"+serializePackagePostfix+"());")
        for i, v in enumerate(a.read_data["emit"][1:]):
            out.append("subscribedBuffersNames["+str(i + 1)+"] = \""+v["name"]+"\";")
            out.append("allWriters["+str(i+1)+"] = w"+str(i+1)+";")
            out.append("allWriters_callbacks["+str(i+1)+"] = new "+deserializatorPath+"(new "+".".join(v["type"].split(".")[:-1])+serializePackagePostfix+"());")

    if len(a.read_data["receive"]) - 1 > 0:
        out.append("publishedBuffersNames = new String["+str(len(a.read_data["receive"]) - 1 + 1)+"]"+";")
        out.append("allReaders = new reader["+str(len(a.read_data["receive"]) - 1 + 1)+"]"+";")
        out.append("allReaders_callbacks = new serializeStreamCallback["+str(len(a.read_data["receive"]) - 1 + 1)+"]"+";")
        out.append("publishedBuffersNames[0] = \"nodeRepository\";")
        out.append("allReaders_callbacks[0] = new "+serializatorPath+"(new com.github.osblinnikov.cnetsTransports.nodeRepositoryProtocol"+serializePackagePostfix+"());")
        for i, v in enumerate(a.read_data["receive"][1:]):
            out.append("publishedBuffersNames["+str(i + 1)+"] = \""+v["name"]+"\";")
            out.append("allReaders["+str(i+1)+"] = r"+str(i+1)+";")
            out.append("allReaders_callbacks["+str(i+1)+"] = new "+serializatorPath+"(new "+".".join(v["type"].split(".")[:-1])+serializePackagePostfix+"());")


    return "\n    ".join(out)