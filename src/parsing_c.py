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
    if v.has_key("size") and v["size"] != None:
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
    arr.append("selector_cnets_osblinnikov_github_com readersSelector")

  out = "  "+';\n  '.join(arr)+';\n' if len(arr)>0 else ''
  return out

def getArgs(a):
  out = ""
  argsArray = ["struct "+a.fullName_+" *that"]
  for v in a.read_data["args"]:
    t, isObject, isArray, isSerializable = filterTypes_c(v["type"])
    # v["type"] = t
    argsArray.append(getFullName_(t)+" _"+v["name"])

  for i,v in enumerate(a.read_data["emit"]):
    argsArray.append("writer _w"+v["channel"]+str(i))#v["type"]

  for i,v in enumerate(a.read_data["receive"]):
    argsArray.append("reader _r"+v["channel"]+str(i))#

  return ',\n    '.join(argsArray)

def getDeinit(a):
  out = ""
  for value in a.read_data["props"]:
    # print value
    t, isObject, isArray, isSerializable = filterTypes_c(value["type"])
    if isArray:
      out += "\n  arrayObject_free_dynamic(that->"+value["name"]+");"

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
    out += "\n  arrayObject_free_dynamic(that->readersSelector.reducableReaders);"
    out += "\n  selector_cnets_osblinnikov_github_com_deinit(&that->readersSelector);"

  for v in a.read_data["channels"]:
    out += "\n  "+getFullName_(v["name"])+"_deinit(&that->"+v["channel"]+");"

  hasParallel = "0"
  for i,v in enumerate(a.read_data["topology"]):
    if v["parallel"] != None and v["parallel"] != 1:
      prefixParallel = ""
      if not isinstance(v["parallel"], int ):
        prefixParallel = "that->"
      hasParallel += "+"+prefixParallel+str(v["parallel"])
      out += "\n  int _kernel"+str(i)+"_i;"
      out += "\n  for(_kernel"+str(i)+"_i=0;_kernel"+str(i)+"_i<(int)"+prefixParallel+str(v["parallel"])+";_kernel"+str(i)+"_i++){"
      out += "\n    "+getFullName_(v["name"])+"_deinit(&that->kernel"+str(i)+"[_kernel"+str(i)+"_i]);"
      out += "\n  }"
      out += "\n  free((void*)that->kernel"+str(i)+");"
    else:
      out += "\n  "+getFullName_(v["name"])+"_deinit(&that->kernel"+str(i)+");"
      hasParallel += "+1"
  if hasParallel != "0":
    out += "\n  free((void*)that->arrContainers);"

  return out

def getInit(a):
  out = ""
  for value in a.read_data["args"]:
    out += "\n  that->"+value["name"]+" = _"+value["name"]+";"


  for i,v in enumerate(a.read_data["emit"]):
    out += "\n  that->w"+v["channel"]+str(i)+" = _w"+v["channel"]+str(i)+";"
  for i,v in enumerate(a.read_data["receive"]):
    out += "\n  that->r"+v["channel"]+str(i)+" = _r"+v["channel"]+str(i)+";"

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
    out += "\n  struct arrayObject _arrReaders_ = arrayObject_init_dynamic(sizeof(reader), "+selectablesCount+");"

    lastId = 0
    for i,v in enumerate(a.read_data["receive"]):
      out += "\n  ((reader*)_arrReaders_.array)["+str(i)+"] = _r"+v["channel"]+str(i)+";"
      lastId = i
    if len(selectableArgs)>0:
      out += "\n  int totalLength = "+str(lastId + 1)+";"
      for i,v in enumerate(selectableArgs):
        out += "\n  for(int i=0;i<"+str(v["name"])+".length; i++){"
        out += "\n    ((reader*)_arrReaders_.array)[totalLength + i] = "+v["name"]+"[i];"
        out += "\n  }"
        if i+1 != len(selectableArgs):
          out += "\n  totalLength += "+str(v["name"])+".length;"
    out += "\n  selector_cnets_osblinnikov_github_com_init(&that->readersSelector, _arrReaders_);"
    out += "\n  that->rSelect = selector_cnets_osblinnikov_github_com_createReader(&that->readersSelector, 0);"
  
  for value in a.read_data["props"]:
    # print value
    t, isObject, isArray, isSerializable = filterTypes_c(value["type"])
    if value["value"]!=None:
      out += "\n  that->"+value["name"]+" = "+value["value"]+";"
    elif isArray:
      arrItemType, itemIsObject, itemIsArray, itemisSerializable = filterTypes_c(value["type"][:-2])
      if isinstance(value["size"], basestring):
        value["size"] = "that->"+value["size"]
      out += "\n  that->"+value["name"]+" = arrayObject_init_dynamic(sizeof("+getFullName_(arrItemType)+"), "+str(value["size"])+");"

  
  # for i,v in enumerate(a.read_data["props"]):
  #   if v["value"]!=None:
  #     out += "\\\n    _NAME_."+v["name"]+" = "+v["value"]+";"  
  # out += "\n  "+a.fullName_+"_initialize(&_NAME_);"

  return out

# def getReaderWriterArgumentsStrarrDel0(a):
#   readerWriterArgumentsStrArr = []

#   readerWriterArguments = a.rwArguments
#   if readerWriterArguments[0]["name"] != "gridId":
#     raise Exception("getReaderWriterArgumentsStrArr: readerWriterArguments[0][\"name\"]!=\"gridId\"")
#   for value in readerWriterArguments:
#     if value["type"] == "unsigned":
#       value["type"] = "int"
#     readerWriterArgumentsStrArr.append(value["type"]+" "+value["name"])

#   del readerWriterArgumentsStrArr[0]
#   return readerWriterArgumentsStrArr

# def getContainerClass(a):
#   arrDel0 = getReaderWriterArgumentsStrarrDel0(a)
#   out = ""
#   if len(arrDel0)>0:
#     out += "\ntypedef struct "+a.fullName_+"_container{"
#     for rwArg in arrDel0:
#       out += "\n  "+rwArg+";"
#     out += "\n}"+a.fullName_+"_container;"
#   return out


# def getReaderWriterArgumentsStr(a):
#   readerWriterArgumentsStrArr = ["_NAME_","_that"]

#   readerWriterArguments = a.rwArguments
#   if readerWriterArguments[0]["name"] != "gridId":
#     raise Exception("getReaderWriterArgumentsStrArr: readerWriterArguments[0][\"name\"]!=\"gridId\"")
#   for value in readerWriterArguments:
#     if value["type"] == "unsigned":
#       value["type"] = "int"
#     readerWriterArgumentsStrArr.append("_"+value["name"])

#   return ','.join(readerWriterArgumentsStrArr)

# def getReaderWriter(a):
#   out = ""
#   out += "#define "+a.fullName_+"_createReader("+getReaderWriterArgumentsStr(a)+")"
#   if len(a.rwArguments) == 0:
#     raise Exception("len(a.rwArguments) == 0")
#   elif len(a.rwArguments) > 1:
#     out += "\\\n  "+a.fullName_+"_container _NAME_##_container;"
#     for value in a.rwArguments:
#       if value['name'] != "gridId":
#         out += "\\\n  _NAME_##_container."+value['name']+" = _"+value["name"]+";"
#     out += "\\\n  reader _NAME_ = "+a.fullName_+"_getReader(_that,(void*)&_NAME_##_container,_gridId);"
#   else:
#     out += "\\\n  reader _NAME_ = "+a.fullName_+"_getReader(_that,NULL,_gridId);"
  

#   out += "\n\n#define "+a.fullName_+"_createWriter("+getReaderWriterArgumentsStr(a)+")"
#   if len(a.rwArguments) == 0:
#     raise Exception("len(a.rwArguments) == 0")
#   elif len(a.rwArguments) > 1:
#     out += "\\\n  "+a.fullName_+"_container _NAME_##_container;"
#     for value in a.rwArguments:
#       if value['name'] != "gridId":
#         out += "\\\n  _NAME_##_container."+value['name']+" = _"+value["name"]+";"
#     out += "\\\n  writer _NAME_ = "+a.fullName_+"_getWriter(_that,(void*)&_NAME_##_container,_gridId);"
#   else:
#     out += "\\\n  writer _NAME_ = "+a.fullName_+"_getWriter(_that,NULL,_gridId);"

#   return out

def directoryFromBlockPath(path):
  pathList = splitClassPath(path)
  domain = pathList[0]
  del pathList[0]
  domain = pathList[0]+"."+domain
  del pathList[0]
  fileName = pathList[-1]
  # del pathList[-1]
  return '/'.join([domain]+pathList+[fileName])

def importBlocks(a):
  dependenciesDict = getDependenciesDict(a.read_data)
  out = ""
  for v  in dependenciesDict:
    out+="\n#include \""+directoryFromBlockPath(v["name"])+".h\""
  return out

def declareBlocks(a):
  out = ""
  hasParallel = False
  for i,v in enumerate(a.read_data["topology"]):
    # pathList = v["path"].split('.')
    if v["parallel"]!=None and v["parallel"] != 1:
      hasParallel = True
      out += getFullName_(v["name"])+"* kernel"+str(i)+";\n  "
    else:
      out += getFullName_(v["name"])+" kernel"+str(i)+";\n  "

  for i,v in enumerate(a.read_data["channels"]):
    out += getFullName_(v["name"])+" "+v["channel"]+";\n  "

  a.sizeRunnables = 0
  for k,v in enumerate(a.read_data["topology"]):
    if v.has_key("type") and v["type"] == "buffer":
      continue
    a.sizeRunnables += 1

  if a.sizeRunnables > 0:
    if hasParallel:
      out += "\nrunnablesContainer_cnets_osblinnikov_github_com* arrContainers;\n  "
    else:
      out += "\nrunnablesContainer_cnets_osblinnikov_github_com arrContainers["+str(a.sizeRunnables)+"];\n  "
  return out

def isChannelInStorage(w, storage):
  for i, v in enumerate(storage):
    if v["channel"] == w["channel"]:
      w["pinId"] = i
      if not v.has_key("name") or v["name"] == None:
        v["name"] = DefaultMapBuffer
      return True
  return False


def getReadersWriters(a,v,tid):
  arr = []
  #set writer to the buffer
  for i,w in enumerate(v["emit"]):
    if isChannelInStorage(w, a.read_data["emit"]):
      arr.append("that->w"+w["channel"]+str(w["pinId"]))
    elif isChannelInStorage(w, a.read_data["channels"]):
      arr.append(w["channel"]+"w"+str(w["pinId"])+"_"+str(tid))
    else:
      raise Exception("Channel "+w["channel"]+" was not found neither in emit nor channels fields")

  #TODO FINISH HERE WITH THE FOLLOWING 
  for i,w in enumerate(v["receive"]):
    if isChannelInStorage(w, a.read_data["receive"]):
      arr.append("that->r"+w["channel"]+str(w["pinId"]))
    elif isChannelInStorage(w, a.read_data["channels"]):
      arr.append(w["channel"]+"r"+str(w["pinId"])+"_"+str(tid))
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

def getRwArgs(gridId,w):
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
  for v in a.read_data["channels"]:
    # if not v.has_key("type") or v["type"] != "buffer":
    #   continue
    # pathList = v["name"].split('.')
    argsList = []
    for d in v["args"]:
      castType = ""
      if d.has_key("type") and d["type"] != None:
        t, isObject, isArray ,isSerializable = filterTypes_c(d["type"])
        if t != "arrayObject":
          castType = "("+getFullName_(t)+")"
      argValue = str(d["value"])
      if searchPropertyAndArgName(a,d["value"]):
        argValue = "that->"+argValue
      argsList.append(castType+argValue)

    argsList = ["&that->"+v["channel"]]+argsList
    #create variables
    out += "\n  "+getFullName_(v["name"])+"_init("+','.join(argsList)+");"

  for tid, v in enumerate(a.read_data["topology"]):
    #get writer from buffer
    for i,w in enumerate(v["emit"]):
      if isChannelInStorage(w, a.read_data["emit"]):
        # arr.append(
        out += ""
        # out += "\n  that->w"+w["channel"]+str(w["pinId"])+" = _w"+w["channel"]+str(w["pinId"])
      elif isChannelInStorage(w, a.read_data["channels"]):
        chan = a.read_data["channels"][w["pinId"]]
        if not chan.has_key("reader"):
          # print "CHANNEL ======> "+str(w["pinId"])+": "+chan["channel"]+" READER SET 0"
          chan["reader"] = 0
        else:
          chan["reader"]+= 1
          # print "CHANNEL ======> "+str(w["pinId"])+": "+chan["channel"]+" READER SET "+str(chan["reader"])
        out += "\n  writer "+w["channel"]+"w"+str(w["pinId"])+"_"+str(tid)+" = "+getFullName_(chan["name"])+"_createWriter("+','.join([ "&that->"+w["channel"]] + getRwArgs(chan["reader"],w))+");"
      else:
        raise Exception("Channel "+w["channel"]+" was not found neither in emit nor channels fields")
      
      # connectBufferToReader(a, blockNum, i, w)
    #get reader from buffer
    for i,w in enumerate(v["receive"]):
      if isChannelInStorage(w, a.read_data["receive"]):
        # arr.append(
        out += ""
        # out += "\n  that->r"+w["channel"]+str(w["pinId"])+" = _r"+w["channel"]+str(w["pinId"])
      elif isChannelInStorage(w, a.read_data["channels"]):
        chan = a.read_data["channels"][w["pinId"]]
        if not chan.has_key("writer"):
          # print "CHANNEL ======> "+str(w["pinId"])+": "+chan["channel"]+" WRITER SET 0"
          chan["writer"] = 0
        else:
          chan["writer"]+= 1
          # print "CHANNEL ======> "+str(w["pinId"])+": "+chan["channel"]+" WRITER SET "+str(chan["writer"])
          
        out += "\n  reader "+w["channel"]+"r"+str(w["pinId"])+"_"+str(tid)+" = "+getFullName_(chan["name"])+"_createReader("+','.join([ "&that->"+w["channel"]] + getRwArgs(chan["writer"],w))+");"
      else:
        raise Exception("Channel "+w["channel"]+" was not found neither in emit nor channels fields")
      
      # out += "\n    "+getFullName_(v["name"])+"_createWriter("+','.join([ "_NAME_##"+v["channel"]+"w"+str(i),  "&_NAME_."+v["channel"]] + getRwArgs(i,w))+")"
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
      if d.has_key("type") and d["type"] != None:
        t, isObject, isArray, isSerializable = filterTypes_c(d["type"])
        if t != "arrayObject":
          castType = "("+getFullName_(t)+")"
      argValue = str(d["value"])
      if searchPropertyAndArgName(a,d["value"]):
        argValue = "that->"+argValue
      argsList.append(castType+argValue)
    if v["parallel"] != None and v["parallel"] != 1:
      prefixParallel = ""
      if not isinstance(v["parallel"], int ):
        prefixParallel = "that->"
      hasParallel += "+"+prefixParallel+str(v["parallel"])
      out += "\n  that->kernel"+str(i)+" = ("+getFullName_(v["name"])+"*)malloc(sizeof("+getFullName_(v["name"])+")*"+prefixParallel+str(v["parallel"])+");"
      out += "\n  int _kernel"+str(i)+"_i;"
      out += "\n  for(_kernel"+str(i)+"_i=0;_kernel"+str(i)+"_i<(int)"+prefixParallel+str(v["parallel"])+";_kernel"+str(i)+"_i++){"
      out += "\n    "+getFullName_(v["name"])+"_init("+','.join(["&that->kernel"+str(i)+"[_kernel"+str(i)+"_i]"]+argsList+getReadersWriters(a,v,i))+");"
      out += "\n  }"
    else:
      out += "\n  "+getFullName_(v["name"])+"_init("+','.join(["&that->kernel"+str(i)]+argsList+getReadersWriters(a,v,i))+");"
      hasParallel += "+1"
  if hasParallel != "0":
    out += "\n  that->arrContainers = (runnablesContainer_cnets_osblinnikov_github_com*)malloc(sizeof(runnablesContainer_cnets_osblinnikov_github_com)*("+evalSize(hasParallel)+"));"
  return out

def runBlocks(a):
  out = []
  hasParallel = False
  #kernels
  for i,v in enumerate(a.read_data["topology"]):
    # if v.has_key("type") and v["type"] == "buffer":
    #   continue
    if v["parallel"]!=None and v["parallel"] != 1:
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
  argsList = ["&classObj"]
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

  out = a.fullName_+" classObj;\n  "
  out += a.fullName_+"_init("+getDefaultRunParameters(a)+");"
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

  out = a.fullName_+" classObj;\n  "
  out += a.fullName_+"_init("+getDefaultRunParameters(a)+");"
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
  for i, v in enumerate(a.read_data["topology"]):
    # if v.has_key("type") and v["type"] == "buffer":
    #   continue
    if v["parallel"]!=None and v["parallel"] != 1:
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
    runnablesContainer_cnets_osblinnikov_github_com runnables;
    runnablesContainer_cnets_osblinnikov_github_com_init(&runnables);
    RunnableStoppable_create(runnableStoppableObj,that, '''+a.fullName_+'''_)
    runnables.setCore(&runnables,runnableStoppableObj);
    return runnables;'''
  else:
    return  '''
    runnablesContainer_cnets_osblinnikov_github_com runnables;
    runnablesContainer_cnets_osblinnikov_github_com_init(&runnables);
    '''+out+'''
    arrayObject arr;
    arr.array = (void*)that->arrContainers;
    arr.length = '''+str(evalSize(sizeRunnables))+''';
    arr.itemSize = sizeof(runnablesContainer_cnets_osblinnikov_github_com);
    runnables.setContainers(&runnables,arr);
    return runnables;'''