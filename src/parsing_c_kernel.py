import json
import re
from gernetHelpers import *
import operator

def recurseDependencies(dependenciesDict):
  newDependenciesDict = dict()
  hasNewData = False
  for k,v in dependenciesDict.items():
    read_data = readJson(os.path.join(PROJECTS_ROOT_PATH,getPath(v["path"]),'gernet.json') )
    if read_data == None:
      continue
    for v in read_data["topology"]+read_data["depends"]:
      if not dependenciesDict.has_key(v["path"]) and not newDependenciesDict.has_key(v["path"]):
        newDependenciesDict[v["path"]] = v
        hasNewData = True
  if hasNewData:
    newDependenciesDict = recurseDependencies(newDependenciesDict)
    i = len(dependenciesDict)
    for k,v in newDependenciesDict.items():
      if not dependenciesDict.has_key(v["path"]):
        dependenciesDict[v["path"]] = v
        dependenciesDict[v["path"]]['_order'] = i
        i = i + 1
  return dependenciesDict

def getDependenciesList(a):
  dependenciesDict = dict()


  i = len(dependenciesDict)
  for v in a.read_data["topology"]+a.read_data["depends"]:
    if not dependenciesDict.has_key(v["path"]):
      dependenciesDict[v["path"]] = v
      dependenciesDict[v["path"]]['_order'] = i
      i = i + 1

  dependenciesDict = recurseDependencies(dependenciesDict)

  #sorting
  dictToSort = dict()
  for k,v in dependenciesDict.items():
    dictToSort[v["_order"]] = v
  
  return sorted(dictToSort.items(), key=operator.itemgetter(0))


def getReaderWriterArgumentsStrarrDel0(a):
  readerWriterArgumentsStrArr = []

  readerWriterArguments = a.rwArguments
  if readerWriterArguments[0]["name"] != "gridId":
    raise Exception("getReaderWriterArgumentsStrArr: readerWriterArguments[0][\"name\"]!=\"gridId\"")
  for value in readerWriterArguments:
    if value["type"] == "unsigned":
      value["type"] = "int"
    readerWriterArgumentsStrArr.append(value["type"]+" "+value["name"])

  del readerWriterArgumentsStrArr[0]
  return readerWriterArgumentsStrArr

def getReaderWriterArgumentsStr(a):
  readerWriterArgumentsStrArr = ["_NAME_","_that"]

  readerWriterArguments = a.rwArguments
  if readerWriterArguments[0]["name"] != "gridId":
    raise Exception("getReaderWriterArgumentsStrArr: readerWriterArguments[0][\"name\"]!=\"gridId\"")
  for value in readerWriterArguments:
    if value["type"] == "unsigned":
      value["type"] = "int"
    readerWriterArgumentsStrArr.append("_"+value["name"])

  return ','.join(readerWriterArgumentsStrArr)

def getFieldsArrStr(a):
  arr = []
  props = []
  if a.read_data.has_key("props"):
    props = a.read_data["props"]
  for v in a.read_data["args"]+props:
    t, isObject, isArray, isSerializable = filterTypes_c(v["type"])
    if v.has_key("size"):
      if not isArray:
        raise Exception("getFieldsArrStr: size of property "+str(v["name"])+" was specified but type is not array!")
    # if isArray:
    #   if not v.has_key("size")
    #     arr.append(v["type"][:-2]+" _"+v["name"]+"_["+str(v["size"])+"]")
      # else:
      #   raise Exception("prop "+v["type"]+" "+v["name"]+" is Array, but size was not specified")
    # v["type"] = t
    arr.append(artifactId(t)+" "+v["name"])

  for i,v in enumerate(a.read_data["emit"]):
    arr.append("writer w"+str(i))

  for i,v in enumerate(a.read_data["receive"]):
    arr.append("reader r"+str(i))


  noSelectors = False
  if a.read_data.has_key("noSelectors"):
      noSelectors = a.read_data["noSelectors"]
  if len(a.read_data["receive"]) > 1 and not noSelectors:
    arr.append("reader rSelect")
    arr.append("selector_cnets_osblinnikov_github_com readersSelector")

  return arr

def getargsArrStrs(a):
  arr = ["_NAME_"]
  for v in a.read_data["args"]:
    t, isObject, isArray, isSerializable = filterTypes_c(v["type"])
    # v["type"] = t
    arr.append("_"+v["name"])

  for i,v in enumerate(a.read_data["emit"]):
    arr.append("_w"+str(i))

  for i,v in enumerate(a.read_data["receive"]):
    arr.append("_r"+str(i))

  return arr

def groupId(path):
  path = path.split(".")
  del path[-1]
  return '.'.join(path)

def artifactId(path):
  fullNameList = path.split('.')
  return '_'.join(fullNameList)

def getPath(path):
  path = path.split('.')
  arr = []
  arr.append(path[1]+"."+path[0])
  to_delete = [0,1]
  for offset, index in enumerate(to_delete):
    index -= offset
    del path[index]
  return '/'.join(arr+path)

def parsingGernet(a):

  a.read_data = None
  a.read_data = readJson(a.prefix)

  fullName = a.read_data["path"]
  a.fullName_ = artifactId(fullName)
  # a.version = a.read_data["ver"]
  fullNameList = fullName.split('.')
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
  # a.arrDel0 = getReaderWriterArgumentsStrarrDel0(a.rwArguments)
  a.rwArgumentsStr = getReaderWriterArgumentsStr(a)

def getProps(a):
  fieldsArray = getFieldsArrStr(a)
  out = "  "+';'.join(fieldsArray)+';\n' if len(fieldsArray)>0 else ''
  return out

def getConstructor(a):
  out = ""
  argsArray = getargsArrStrs(a)
  out += "#define "+a.fullName_+"_create("+','.join(argsArray)+")"
  out += "\\\n    "+a.fullName_+" _NAME_;"
  for value in a.read_data["args"]:
    out += "\\\n    _NAME_."+value["name"]+" = _"+value["name"]+";"

  #SELECTABLE

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
    out += "\\\n    arrayObject_create(_NAME_##_arrReaders_, reader, "+selectablesCount+")"

    lastId = 0
    for i,v in enumerate(a.read_data["receive"]):
      out += "\\\n    ((reader*)_NAME_##_arrReaders_.array)["+str(i)+"] = _r"+str(i)+";"
      lastId = i
    if len(selectableArgs)>0:
      out += "\\\n    int totalLength = "+str(lastId + 1)+";"
      for i,v in enumerate(selectableArgs):
        out += "\\\n    for(int i=0;i<"+str(v["name"])+".length; i++){"
        out += "\\\n      ((reader*)_NAME_##_arrReaders_.array)[totalLength + i] = "+v["name"]+"[i];"
        out += "\\\n    }"
        if i+1 != len(selectableArgs):
          out += "\\\n    totalLength += "+str(v["name"])+".length;"
    out += "\\\n    selector_cnets_osblinnikov_github_com_create(_NAME_##readersSelector, _NAME_##_arrReaders_);"
    out += "\\\n    _NAME_.readersSelector = _NAME_##readersSelector;"
    out += "\\\n    selector_cnets_osblinnikov_github_com_createReader(_NAME_##_rSelect_,&_NAME_.readersSelector,-1,0)"
    out += "\\\n    _NAME_.rSelect = _NAME_##_rSelect_;"

  #END OF ARGS AND SELECTABLE ARG


  out += "\\\n    "+a.fullName_+"_onCreateMacro(_NAME_)"

  if a.read_data.has_key("props"):
    for value in a.read_data["props"]:
      t, isObject, isArray, isSerializable = filterTypes_c(value["type"])
      if value.has_key("value"):
        out += "\\\n    _NAME_."+value["name"]+" = "+value["value"]+";"
      elif isArray:
        arrItemType, itemIsObject, itemIsArray, itemisSerializable = filterTypes_c(value["type"][:-2])
        if isinstance(value["size"], basestring):
          value["size"] = "_"+value["size"]
        out += "\\\n    arrayObject_create(_NAME_##_"+value["name"]+"_, "+'_'.join(arrItemType.split('.'))+", "+str(value["size"])+")"
        out += "\\\n    _NAME_."+value["name"]+" = _NAME_##_"+value["name"]+"_;"


  for i,v in enumerate(a.read_data["emit"]):
    out += "\\\n    _NAME_.w"+str(i)+" = _w"+str(i)+";"
  for i,v in enumerate(a.read_data["receive"]):
    out += "\\\n    _NAME_.r"+str(i)+" = _r"+str(i)+";"
  
  if a.read_data.has_key("props"):
    for i,v in enumerate(a.read_data["props"]):
      if v.has_key("value"):
        out += "\\\n    _NAME_."+v["name"]+" = "+v["value"]+";"  
  out += "\\\n    "+a.fullName_+"_initialize(&_NAME_);"
  out += initializeBuffers(a)
  out += "\\\n    "+a.fullName_+"_onKernels(&_NAME_);"
  out += initializeKernels(a)
  return out

def getContainerClass(a):
  arrDel0 = getReaderWriterArgumentsStrarrDel0(a)
  out = ""
  if len(arrDel0)>0:
    out += "\ntypedef struct "+a.fullName_+"_container{"
    for rwArg in arrDel0:
      out += "\n  "+rwArg+";"
    out += "\n}"+a.fullName_+"_container;"
  return out

def getReaderWriter(a):
  out = ""
  out += "#define "+a.fullName_+"_createReader("+a.rwArgumentsStr+")"
  if len(a.rwArguments) == 0:
    raise Exception("len(a.rwArguments) == 0")
  elif len(a.rwArguments) > 1:
    out += "\\\n  "+a.fullName_+"_container _NAME_##_container;"
    for value in a.rwArguments:
      if value['name'] != "gridId":
        out += "\\\n  _NAME_##_container."+value['name']+" = _"+value["name"]+";"
    out += "\\\n  reader _NAME_ = "+a.fullName_+"_getReader(_that,(void*)&_NAME_##_container,_gridId);"
  else:
    out += "\\\n  reader _NAME_ = "+a.fullName_+"_getReader(_that,NULL,_gridId);"
  

  out += "\n\n#define "+a.fullName_+"_createWriter("+a.rwArgumentsStr+")"
  if len(a.rwArguments) == 0:
    raise Exception("len(a.rwArguments) == 0")
  elif len(a.rwArguments) > 1:
    out += "\\\n  "+a.fullName_+"_container _NAME_##_container;"
    for value in a.rwArguments:
      if value['name'] != "gridId":
        out += "\\\n  _NAME_##_container."+value['name']+" = _"+value["name"]+";"
    out += "\\\n  writer _NAME_ = "+a.fullName_+"_getWriter(_that,(void*)&_NAME_##_container,_gridId);"
  else:
    out += "\\\n  writer _NAME_ = "+a.fullName_+"_getWriter(_that,NULL,_gridId);"

  return out

def directoryFromBlockPath(path):
  pathList = path.split('.')
  domain = pathList[0]
  del pathList[0]
  domain = pathList[0]+"."+domain
  del pathList[0]
  fileName = pathList[-1]
  # del pathList[-1]
  return '/'.join([domain]+pathList+["c","include",fileName])

def importBlocks(a):
  dependenciesDict = dict()
  for v in a.read_data["topology"]+a.read_data["depends"]:
    dependenciesDict[v["path"]] = v
  out = ""
  for k,v  in dependenciesDict.items():
    out+="\n#include \""+directoryFromBlockPath(v["path"])+".h\""
  return out

def declareBlocks(a):
  out = ""
  hasParallel = False
  for v in a.read_data["topology"]:
    pathList = v["path"].split('.')
    if v.has_key("parallel"):
      hasParallel = True
      out += "_".join(pathList)+"* "+v["name"]+";"
    else:
      out += "_".join(pathList)+" "+v["name"]+";"

  a.sizeRunnables = 0
  for k,v in enumerate(a.read_data["topology"]):
    if v.has_key("type") and v["type"] == "buffer":
      continue
    a.sizeRunnables += 1

  if a.sizeRunnables > 0:
    if hasParallel:
      out += "\nrunnablesContainer_cnets_osblinnikov_github_com* arrContainers;"
    else:
      out += "\nrunnablesContainer_cnets_osblinnikov_github_com arrContainers["+str(a.sizeRunnables)+"];"
  return out

def checkPinId(arrPins, pinId):
    for i,pin in enumerate(arrPins):
        if pin.has_key("gridId"):
            gridId = pin["gridId"]
            if gridId == pinId:
                if pin.has_key("is_busy"):
                    return -1
                pin["is_busy"] = True
                return i
    if len(arrPins)>pinId:
        pin = arrPins[pinId]
        if pin.has_key("is_busy"):
            return -1
        pin["is_busy"] = True
        return pinId
    else:
        return -1

def getReadersWriters(a,v, curBlock):
  arr = []
  #set writer to the buffer
  for i,w in enumerate(v["emit"]):
    blockId = w["blockId"]
    if blockId == "export":
      if checkPinId(a.read_data["emit"], w["pinId"]) != -1:
        arr.append("_NAME_.w"+str(w["pinId"]))
      else:
        raise Exception("pinId _NAME_.w."+str(w["pinId"])+" was not found in the exported connection")
    elif blockId != "internal":
      rblock = a.read_data["topology"][int(blockId)]
      if rblock["type"] != "buffer":
        raise Exception("Connection from the block allowed only to the block with type='buffer'")
      # r = rblock["receive"]
      if checkPinId(rblock["receive"], w["pinId"]) != -1:
        arr.append("_NAME_##"+rblock["name"]+"w"+str(w["pinId"]))
      else:
        raise Exception("pinId w."+str(w["pinId"])+" was not found in the destination buffer")

  #get reader from buffer
  for i,r in enumerate(v["receive"]):
    blockId = r["blockId"]
    if blockId == "export":
      if checkPinId(a.read_data["receive"], r["pinId"]) != -1:
        arr.append("_NAME_.r"+str(r["pinId"]))
      else:
        raise Exception("pinId _NAME_.r."+str(r["pinId"])+" was not found in the exported connection")
    elif blockId != "internal":
      wblock = a.read_data["topology"][int(blockId)]
      if wblock["type"] != "buffer":
        raise Exception("Connection from the block allowed only to the block with type='buffer'")
      # r = wblock["emit"]
      if checkPinId(wblock["emit"], r["pinId"]) != -1:
        arr.append("_NAME_##"+wblock["name"]+"r"+str(r["pinId"]))
      else:
        raise Exception("pinId r."+str(r["pinId"])+" was not found in the destination buffer")
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
      raise Exception("pinId w."+str(w["pinId"])+" was not found in the destination buffer")
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

def searchPropertyAndArgName(a, propName):
  props = []
  if a.read_data.has_key("props"):
    props = a.read_data["props"]
  for v in a.read_data["args"]+props:
    if v["name"] == propName:
      return True
  return False

def initializeBuffers(a):
  out = ""
  #buffers
  for blockNum, v in enumerate(a.read_data["channels"]):
    # if not v.has_key("type") or v["type"] != "buffer":
    #   continue
    pathList = v["path"].split('.')
    argsList = []
    for d in v["args"]:
      castType = ""
      if d.has_key("type"):
        t, isObject, isArray ,isSerializable = filterTypes_c(d["type"])
        if t != "arrayObject":
          castType = "("+t+")"
      argValue = str(d["value"])
      if searchPropertyAndArgName(a,d["value"]):
        argValue = "_NAME_."+argValue
      argsList.append(castType+argValue)
    #create variables
    out += "\\\n    "+'_'.join(pathList)+"_create("+','.join([v["name"]]+argsList)+")"
    out += "\\\n    _NAME_."+v["name"]+" = "+v["name"]+";"
    #get writer from buffer
    for i,w in enumerate(v["emit"]):
      out += "\\\n    "+'_'.join(pathList)+"_createReader("+','.join([ "_NAME_##"+v["name"]+"r"+str(i),  "&_NAME_."+v["name"]] + getRwArgs(i,w))+")"
      connectBufferToReader(a, blockNum, i, w)
    #get reader from buffer
    for i,w in enumerate(v["receive"]):
      out += "\\\n    "+'_'.join(pathList)+"_createWriter("+','.join([ "_NAME_##"+v["name"]+"w"+str(i),  "&_NAME_."+v["name"]] + getRwArgs(i,w))+")"
  return out

def initializeKernels(a):
  out = ""
  #kernels
  hasParallel = "0"
  for i,v in enumerate(a.read_data["topology"]):
    if v.has_key("type") and v["type"] == "buffer":
      continue
    pathList = v["path"].split('.')
    argsList = []
    for d in v["args"]:
      castType = ""
      if d.has_key("type"):
        t, isObject, isArray, isSerializable = filterTypes_c(d["type"])
        if t != "arrayObject":
          castType = "("+t+")"
      argValue = str(d["value"])
      if searchPropertyAndArgName(a,d["value"]):
        argValue = "_NAME_."+argValue
      argsList.append(castType+argValue)
    if v.has_key("parallel"):
      prefixParallel = ""
      if not isinstance(v["parallel"], int ):
        prefixParallel = "_NAME_."
      hasParallel += "+"+prefixParallel+str(v["parallel"])
      out += "\\\n    "+'_'.join(pathList)+" _NAME_##_"+v["name"]+str(i)+"_##Container["+prefixParallel+str(v["parallel"])+"];"
      out += "\\\n    _NAME_."+v["name"]+" = _NAME_##_"+v["name"]+str(i)+"_##Container;"
      out += "\\\n    int _NAME_##_"+v["name"]+"_##_i;"
      out += "\\\n    for(_NAME_##_"+v["name"]+"_##_i=0;_NAME_##_"+v["name"]+"_##_i<(int)"+prefixParallel+str(v["parallel"])+";_NAME_##_"+v["name"]+"_##_i++){"
      out += "\\\n      "+'_'.join(pathList)+"_create("+','.join([v["name"]]+argsList+getReadersWriters(a,v,i))+");"
      out += "\\\n      _NAME_."+v["name"]+"[_NAME_##_"+v["name"]+"_##_i] = "+v["name"]+";"
      out += "\\\n    }"
    else:
      out += "\\\n    "+'_'.join(pathList)+"_create("+','.join([v["name"]]+argsList+getReadersWriters(a,v,i))+");"
      out += "\\\n    _NAME_."+v["name"]+" = "+v["name"]+";"
      hasParallel += "+1"
  if hasParallel != "0":
    out += "\\\n    runnablesContainer_cnets_osblinnikov_github_com _NAME_##arrContainers["+evalSize(hasParallel)+"];"
    out += "\\\n    _NAME_.arrContainers = _NAME_##arrContainers;"
  return out

def runBlocks(a):
  out = []
  hasParallel = False
  #kernels
  for i,v in enumerate(a.read_data["topology"]):
    if v.has_key("type") and v["type"] == "buffer":
      continue
    if v.has_key("parallel"):
      prefixParallel = ""
      if not isinstance(v["parallel"], int ):
        prefixParallel = "that->"
      if not hasParallel:
        hasParallel = True
        out.append("    int j;")
      out.append("    for(j=0;j<(int)"+prefixParallel+str(v["parallel"])+";j++){")
      out.append("      that->"+v["name"]+"[j].run(&that->"+v["name"]+");")
      out.append("    }")
    else:
      out.append("    that->"+v["name"]+".run(&that->"+v["name"]+");")
  if len(out) > 0:
    return "    "+a.fullName_+" *that = ("+a.fullName_+"*)t;\n"+'\n'.join(out)
  return ''

def getDefaultRunParameters(a):
  argsList = ["classObj"]
  for v in a.read_data["args"]:
    t, isObject, isArray, isSerializable = filterTypes_c(v["type"])
    if v.has_key("value_java"):
      argsList.append(str(v["value_java"]))
    elif v.has_key("value"):
      argsList.append(str(v["value"]))
    elif isArray or isObject:
    #   # t = t[:-2]
    #   argsList.append("new arrayObject")
    # elif isObject:
      argsList.append("arrayObjectNULL()")
    else:
      argsList.append("0")
  for v in a.read_data["emit"]:
    argsList.append("writerNULL()")
  for v in a.read_data["receive"]:
    argsList.append("readerNULL()")
  return ','.join(argsList)

def startRunnables(a):
  typeOfBlock = "kernel"
  if a.read_data.has_key("type"):
    typeOfBlock = a.read_data["type"]

  out = a.fullName_+"_create("+getDefaultRunParameters(a)+");"
  if typeOfBlock == "kernel":
    out += '''
    runnablesContainer_cnets_osblinnikov_github_com runnables = classObj.getRunnables(&classObj);
    runnables.launch(&runnables,TRUE);
    '''
  return out

def testRunnables(a):
  typeOfBlock = "kernel"
  if a.read_data.has_key("type"):
    typeOfBlock = a.read_data["type"]

  out = a.fullName_+"_create("+getDefaultRunParameters(a)+");"
  if typeOfBlock == "kernel":
    out += '''
    runnablesContainer_cnets_osblinnikov_github_com runnables = classObj.getRunnables(&classObj);
    runnables.launch(&runnables,FALSE);
    runnables.stop(&runnables);
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
  out = "\n"
  hasParallel = False
  for blockNum, v in enumerate(a.read_data["topology"]):
    if v.has_key("type") and v["type"] == "buffer":
      continue
    if v.has_key("parallel"):
      prefixParallel = ""
      if not isinstance(v["parallel"], int ):
        prefixParallel = "that->"
      if not hasParallel:
        out += "    int j;\n"
        hasParallel = True
      out += "    for(j=0;j<(int)"+prefixParallel+str(v["parallel"])+";j++){\n"
      out += "      that->arrContainers["+str(evalSize(sizeRunnables))+"+j] = that->"+v["name"]+"[j].getRunnables(&that->"+v["name"]+"[j]);\n"
      out += "    }\n"
      sizeRunnables += "+"+prefixParallel+str(v["parallel"])
    else:
      out += "    that->arrContainers["+str(sizeRunnables)+"] = that->"+v["name"]+".getRunnables(&that->"+v["name"]+");\n"
      sizeRunnables += "+1"

  if sizeRunnables == "0":
    if len(str(a.read_data["spawnMode"])) == 0:
        a.read_data["spawnMode"] = 1
    return '''
    runnablesContainer_cnets_osblinnikov_github_com_create(runnables)
    RunnableStoppable_create(runnableStoppableObj,that, '''+a.fullName_+'''_)
    runnables.setCore(&runnables,runnableStoppableObj, dispatcherCollector_getNextLocalId(), '''+str(a.read_data["spawnMode"])+''');
    return runnables;'''
  else:
    return  '''
    runnablesContainer_cnets_osblinnikov_github_com_create(runnables)
    '''+out+'''
    arrayObject arr;
    arr.array = (void*)&that->arrContainers;
    arr.length = '''+str(evalSize(sizeRunnables))+''';
    arr.itemSize = sizeof(runnablesContainer_cnets_osblinnikov_github_com);
    runnables.setContainers(&runnables,arr);
    return runnables;'''
