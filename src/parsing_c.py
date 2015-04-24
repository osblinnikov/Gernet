import json
import re
from gernetHelpers import *

def parsingGernet(a):

  a.read_data = None
  a.read_data = readYaml(a.prefix)

  fullName = a.read_data["name"]
  a.fullName_ = getFullName_(fullName)
  a.className = getClassName(fullName)
  a.companyDomain = getCompanyDomain(fullName)
  a.company = getCompany(fullName)
  a.domainName = getDomainName(fullName)
  a.domainPath = getDomainPath(fullName)
  a.defaulRwArguments = [{"name":"gridId","type":"unsigned"}]
  a.rwArguments = [{"name":"gridId","type":"unsigned"}]
  if a.read_data.has_key("rwArgs"):
    a.rwArguments+=a.read_data["rwArgs"]

def getProps(a):
  arr = []

  for v in a.read_data["args"]+a.read_data["props"]:
    t, isObject, isArray, isSerializable = filterTypes_c(v["type"])
    if v["size"] != None:
      if not isArray:
        raise Exception("getProps: size of property "+str(v["name"])+" was specified but type is not array!")    
    arr.append(getFullName_(t)+" "+v["name"])

  for i,v in enumerate(a.read_data["emit"]):
    arr.append("writer w"+v["channel"]+str(i))

  for i,v in enumerate(a.read_data["receive"]):
    arr.append("reader r"+v["channel"]+str(i))

  noSelectors = False
  if a.read_data.has_key("noSelectors"):
      noSelectors = a.read_data["noSelectors"]
  if len(a.read_data["receive"]) > 1 and not noSelectors:
    arr.append("reader rSelect")
    arr.append("com_github_osblinnikov_cnets_selector readersSelector")

  out = "  "+';'.join(arr)+';\n' if len(arr)>0 else ''
  return out

def getConstructor(a):
  out = ""

  argsArray = ["_NAME_"]
  for v in a.read_data["args"]:
    t, isObject, isArray, isSerializable = filterTypes_c(v["type"])
    # v["type"] = t
    argsArray.append("_"+v["name"])

  for i,v in enumerate(a.read_data["emit"]):
    argsArray.append("_w"+v["channel"]+str(i))

  for i,v in enumerate(a.read_data["receive"]):
    argsArray.append("_r"+v["channel"]+str(i))

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
    out += "\\\n    com_github_osblinnikov_cnets_selector_create(_NAME_##readersSelector, _NAME_##_arrReaders_);"
    out += "\\\n    _NAME_.readersSelector = _NAME_##readersSelector;"
    out += "\\\n    com_github_osblinnikov_cnets_selector_createReader(_NAME_##_rSelect_,&_NAME_.readersSelector,-1,0)"
    out += "\\\n    _NAME_.rSelect = _NAME_##_rSelect_;"

  #END OF ARGS AND SELECTABLE ARG


  out += "\\\n    "+a.fullName_+"_onCreateMacro(_NAME_)"

  for value in a.read_data["props"]:
    t, isObject, isArray, isSerializable = filterTypes_c(value["type"])
    if value["value"]!=None:
      out += "\\\n    _NAME_."+value["name"]+" = "+value["value"]+";"
    elif isArray:
      arrItemType, itemIsObject, itemIsArray, itemisSerializable = filterTypes_c(value["type"][:-2])
      if isinstance(value["size"], basestring):
        value["size"] = "_"+value["size"]
      out += "\\\n    arrayObject_create(_NAME_##_"+value["name"]+"_, "+getFullName_(arrItemType)+", "+str(value["size"])+")"
      out += "\\\n    _NAME_."+value["name"]+" = _NAME_##_"+value["name"]+"_;"


  for i,v in enumerate(a.read_data["emit"]):
    out += "\\\n    _NAME_.w"+v["channel"]+str(i)+" = _w"+v["channel"]+str(i)+";"
  for i,v in enumerate(a.read_data["receive"]):
    out += "\\\n    _NAME_.r"+v["channel"]+str(i)+" = _r"+v["channel"]+str(i)+";"
  
  for i,v in enumerate(a.read_data["props"]):
    if v["value"]!=None:
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

def getReaderWriter(a):
  out = ""
  out += "#define "+a.fullName_+"_createReader("+getReaderWriterArgumentsStr(a)+")"
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
  

  out += "\n\n#define "+a.fullName_+"_createWriter("+getReaderWriterArgumentsStr(a)+")"
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
  pathList = splitClassPath(path)
  domain = pathList[0]
  del pathList[0]
  domain = pathList[0]+"."+domain
  del pathList[0]
  fileName = pathList[-1]
  # del pathList[-1]
  return '/'.join([domain]+pathList+["c","include",fileName])

def importBlocks(a):
  dependenciesDict = getDependenciesDict(a.read_data)
  out = ""
  for k,v  in dependenciesDict.items():
    out+="\n#include \""+directoryFromBlockPath(v["name"])+".h\""
  return out

def declareBlocks(a):
  out = ""
  hasParallel = False
  for i,v in enumerate(a.read_data["topology"]):
    # pathList = v["path"].split('.')
    if v.has_key("parallel"):
      hasParallel = True
      out += getFullName_(v["name"])+"* kernel"+str(i)+";"
    else:
      out += getFullName_(v["name"])+" kernel"+str(i)+";"

  for i,v in enumerate(a.read_data["channels"]):
    out += getFullName_(v["name"])+" "+v["channel"]+";"

  a.sizeRunnables = 0
  for k,v in enumerate(a.read_data["topology"]):
    if v.has_key("type") and v["type"] == "buffer":
      continue
    a.sizeRunnables += 1

  if a.sizeRunnables > 0:
    if hasParallel:
      out += "\ncom_github_osblinnikov_cnets_runnablesContainer* arrContainers;"
    else:
      out += "\ncom_github_osblinnikov_cnets_runnablesContainer arrContainers["+str(a.sizeRunnables)+"];"
  return out

def isChannelInStorage(w, storage):
  for i, v in enumerate(storage):
    if v["channel"] == w["channel"]:
      w["pinId"] = i
      return True
  return False


def getReadersWriters(a,v,i):
  arr = []
  #set writer to the buffer
  for i,w in enumerate(v["emit"]):
    if isChannelInStorage(w, a["emit"]):
      arr.append("_NAME_.w"+w["channel"]+str(w["pinId"]))
    elif isChannelInStorage(w, a["channels"]):
      arr.append("_NAME_##"+w["channel"]+"w"+str(w["pinId"]))
    else:
      raise Exception("Channel "+w["channel"]+" was not found neither in emit nor channels fields")

  #TODO FINISH HERE WITH THE FOLLOWING 
  for i,w in enumerate(v["receive"]):
    if isChannelInStorage(w, a["receive"]):
      arr.append("_NAME_.w"+w["channel"]+str(w["pinId"]))
    elif isChannelInStorage(w, a["channels"]):
      arr.append("_NAME_##"+w["channel"]+"w"+str(w["pinId"]))
    else:
      raise Exception("Channel "+w["channel"]+" was not found neither in receive nor channels fields")
  return arr

# def connectBufferToReader(a, blockNum, i, w):
#   blockId = w["blockId"]
#   if blockId == "export":
#     raise Exception("Export readerWriter from buffer is forbidden! only kernels can do it [block id = "+str(blockNum)+"]")
#   elif blockId != "internal":
#     wblock = a.read_data["topology"][int(blockId)]
#     if wblock.has_key("type") and wblock["type"] == "buffer":
#       raise Exception("Interconnections of buffers ["+str(blockNum)+" and "+str(blockId)+"] are forbidden")
#     arr_id = checkPinId(wblock["receive"],w["pinId"])
#     if arr_id == -1:
#       raise Exception("pinId w."+str(w["pinId"])+" was not found in the destination buffer")
#     if w["pinId"] != arr_id:
#       raise Exception("wrong parameter gridId!=pinId in the block "+str(blockNum)+", pin "+str(i))

#     pinObject = wblock["receive"][arr_id]
#     if pinObject.has_key("blockId") and pinObject.has_key("pinId") and pinObject["blockId"] != "export":
#       if int(pinObject["blockId"])!=blockNum or int(pinObject["pinId"])!=i:
#         raise Exception("Connection of block "+str(blockNum)+", pin "+str(i)+" with "+str(blockId)+", pin "+str(w["pinId"])+" failed because the last already connected to "+str(pinObject["blockId"])+", "+str(pinObject["pinId"]))
#     pinObject.update({"blockId":blockNum})
#     pinObject.update({"pinId":i})

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
    # pathList = v["name"].split('.')
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
    out += "\\\n    "+getFullName_(v["name"])+"_create("+','.join([v["channel"]]+argsList)+")"
    out += "\\\n    _NAME_."+v["channel"]+" = "+v["channel"]+";"
    #get writer from buffer
    for i,w in enumerate(v["emit"]):
      out += "\\\n    "+getFullName_(v["name"])+"_createReader("+','.join([ "_NAME_##"+v["channel"]+"r"+str(i),  "&_NAME_."+v["channel"]] + getRwArgs(i,w))+")"
      # connectBufferToReader(a, blockNum, i, w)
    #get reader from buffer
    for i,w in enumerate(v["receive"]):
      out += "\\\n    "+getFullName_(v["name"])+"_createWriter("+','.join([ "_NAME_##"+v["channel"]+"w"+str(i),  "&_NAME_."+v["channel"]] + getRwArgs(i,w))+")"
  return out

def initializeKernels(a):
  out = ""
  #kernels
  hasParallel = "0"
  for i,v in enumerate(a.read_data["topology"]):
    # if v.has_key("type") and v["type"] == "buffer":
    #   continue
    # pathList = v["path"].split('.')
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
    if v["parallel"] != None:
      prefixParallel = ""
      if not isinstance(v["parallel"], int ):
        prefixParallel = "_NAME_."
      hasParallel += "+"+prefixParallel+str(v["parallel"])
      out += "\\\n    "+getFullName_(v["name"])+" _NAME_##_kernel"+str(i)+"_##Container["+prefixParallel+str(v["parallel"])+"];"
      out += "\\\n    _NAME_.kernel"+str(i)+" = _NAME_##_kernel"+str(i)+"_##Container;"
      out += "\\\n    int _NAME_##_kernel"+str(i)+"_##_i;"
      out += "\\\n    for(_NAME_##_kernel"+str(i)+"_##_i=0;_NAME_##_kernel"+str(i)+"_##_i<(int)"+prefixParallel+str(v["parallel"])+";_NAME_##_kernel"+str(i)+"_##_i++){"
      out += "\\\n      "+getFullName_(v["name"])+"_create("+','.join(["kernel"]+argsList+getReadersWriters(a,v,i))+");"
      out += "\\\n      _NAME_.kernel"+str(i)+"[_NAME_##_kernel"+str(i)+"_##_i] = kernel;"
      out += "\\\n    }"
    else:
      out += "\\\n    "+getFullName_(v["name"])+"_create("+','.join(["kernel"+str(i)]+argsList+getReadersWriters(a,v,i))+");"
      out += "\\\n    _NAME_.kernel"+str(i)+" = kernel"+str(i)+";"
      hasParallel += "+1"
  if hasParallel != "0":
    out += "\\\n    com_github_osblinnikov_cnets_runnablesContainer _NAME_##arrContainers["+evalSize(hasParallel)+"];"
    out += "\\\n    _NAME_.arrContainers = _NAME_##arrContainers;"
  return out

def runBlocks(a):
  out = []
  hasParallel = False
  #kernels
  for i,v in enumerate(a.read_data["topology"]):
    # if v.has_key("type") and v["type"] == "buffer":
    #   continue
    if v["parallel"]!=None:
      prefixParallel = ""
      if not isinstance(v["parallel"], int ):
        prefixParallel = "that->"
      if not hasParallel:
        hasParallel = True
        out.append("    int j;")
      out.append("    for(j=0;j<(int)"+prefixParallel+str(v["parallel"])+";j++){")
      out.append("      that->kernel"+str(i)+"[j].run(&that->kernel"+str(i)+");")
      out.append("    }")
    else:
      out.append("    that->kernel"+str(i)+".run(&that->kernel"+str(i)+");")
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
    com_github_osblinnikov_cnets_runnablesContainer runnables = classObj.getRunnables(&classObj);
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
    com_github_osblinnikov_cnets_runnablesContainer runnables = classObj.getRunnables(&classObj);
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
  for i, v in enumerate(a.read_data["topology"]):
    # if v.has_key("type") and v["type"] == "buffer":
    #   continue
    if v["parallel"]!=None:
      prefixParallel = ""
      if not isinstance(v["parallel"], int ):
        prefixParallel = "that->"
      if not hasParallel:
        out += "    int j;\n"
        hasParallel = True
      out += "    for(j=0;j<(int)"+prefixParallel+str(v["parallel"])+";j++){\n"
      out += "      that->arrContainers["+str(evalSize(sizeRunnables))+"+j] = that->kernel"+str(i)+"[j].getRunnables(&that->kernel"+str(i)+"[j]);\n"
      out += "    }\n"
      sizeRunnables += "+"+prefixParallel+str(v["parallel"])
    else:
      out += "    that->arrContainers["+str(sizeRunnables)+"] = that->kernel"+str(i)+".getRunnables(&that->kernel"+str(i)+");\n"
      sizeRunnables += "+1"

  if sizeRunnables == "0":
    return '''
    com_github_osblinnikov_cnets_runnablesContainer_create(runnables)
    RunnableStoppable_create(runnableStoppableObj,that, '''+a.fullName_+'''_)
    runnables.setCore(&runnables,runnableStoppableObj);
    return runnables;'''
  else:
    return  '''
    com_github_osblinnikov_cnets_runnablesContainer_create(runnables)
    '''+out+'''
    arrayObject arr;
    arr.array = (void*)&that->arrContainers;
    arr.length = '''+str(evalSize(sizeRunnables))+''';
    arr.itemSize = sizeof(com_github_osblinnikov_cnets_runnablesContainer);
    runnables.setContainers(&runnables,arr);
    return runnables;'''