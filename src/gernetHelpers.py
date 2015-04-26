import yaml
import json
import re
import os
# from config import PROJECTS_ROOT_PATH
from sets import Set
import operator

#PLEASE change it if you don't want the standard workspace root folder location
PROJECTS_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

DefaultMapBuffer = 'github.com/osblinnikov/cnets/mapBuffer'

def readGernet(filename):
    read_data = readYaml(filename+".yaml")
    if read_data != None:
        read_data['prefix'] = filename+".yaml"
    else:
        read_data = readJson(filename+".json")
        if read_data != None:
            read_data['prefix'] = filename+".json"
    # print filename
    # print read_data
    return read_data


def readJson(filename):
    json_file_to_read = os.path.join(filename)
    read_data = None
    try:
        with open (json_file_to_read, "r") as jsonfile:
            # print "opened "+json_file_to_read
            pat=re.compile(r'/\*.*?\*/',re.DOTALL|re.M)
            json_data = re.sub(pat, '', jsonfile.read())
            try:
                read_data = json.loads(json_data)
            except Exception, e:
                print json_file_to_read+" invalid"
                raise e
            jsonfile.close()
    except:
        try:
            jsonfile.close()
        except:
            return read_data

        return read_data

    # print filename
    checkStructure(read_data, False)
    return read_data

def readYaml(filename):
    file_to_read = os.path.join(filename)
    read_data = None
    try:
        with open (file_to_read, "r") as infile:
            pat=re.compile(r'/\*.*?\*/',re.DOTALL|re.M)
            try:
                read_data = yaml.load(re.sub(pat, '', infile.read()))
            except Exception, e:
                print file_to_read+" invalid"
                raise e
            infile.close()
    except:
        try:
            infile.close()
        except:
            return read_data

    # print filename
    checkStructure(read_data, False)
    return read_data

def checkStructure(read_data, isInTopology):
    if not read_data.has_key("name"):
        read_data["name"] = ""

    #EMIT
    if not read_data.has_key("emit"):
        read_data["emit"] = []
    for i,v in enumerate(read_data["emit"]):
        read_data["emit"][i] = parseEmitRecv(v)
        if not isInTopology and read_data["emit"][i]["type"] == None:
            raise Exception(read_data["name"]+" in emit of "+read_data["emit"][i]['channel']+" the type was not set")

    #RECEIVE
    if not read_data.has_key("receive"):
        read_data["receive"] = []
    for i,v in enumerate(read_data["receive"]):
        read_data["receive"][i] = parseEmitRecv(v)
        if not isInTopology and read_data["receive"][i]["type"] == None:
            raise Exception(read_data["name"]+" in receive of "+read_data["receive"][i]['channel']+" the type was not set")

    #Channels
    if isInTopology:
        if not read_data.has_key("parallel"):
            read_data["parallel"] = 1
        if not read_data.has_key("parents"):
            read_data["parents"] = []            
    else:
        if not read_data.has_key("depends"):
            read_data["depends"] = []
        for i,v in enumerate(read_data["depends"]):
            if isinstance( v , basestring ):
                read_data["depends"][i] = {'name': v}

        if not read_data.has_key("spawnMode"):
            read_data["spawnMode"] = ""
        read_data["spawnMode"]="+".join([x for x in Set(read_data["spawnMode"].replace(" ","").split("+")) if (x != "blocking_api" and x != 'monitored')])

        if not read_data.has_key("hide"):
            read_data["hide"] = False        

        #TOPOLOGY
        if not read_data.has_key("topology"):
            read_data["topology"] = []
        for t in read_data["topology"]:
            checkStructure(t, True)
        #PROPS
        if not read_data.has_key("props"):
            read_data["props"] = []
        for i,v in enumerate(read_data["props"]):
            read_data["props"][i] = parseProp(v)

        if not read_data.has_key("channels"):
            read_data["channels"] = []
        for i,v in enumerate(read_data["channels"]):
            read_data["channels"][i] = parseEmitRecvChannels(read_data, v)

    #ARGS
    if not read_data.has_key("args"):
        read_data["args"] = []
    for i,v in enumerate(read_data["args"]):
        read_data["args"][i] = parseArg(v, isInTopology)
   
def getPath(pathSrc):
    # path = pathSrc.split('.')
    # if len(path) < 3:
    #     raise Exception("path: \""+pathSrc+"\" is not a full package name")
    # arr = [PROJECTS_ROOT_PATH, path[1] + "." + path[0]]
    # to_delete = [0, 1]
    # for offset, index in enumerate(to_delete):
    #     index -= offset
    #     del path[index]
    # return '/'.join(arr + path)
    return os.path.join(PROJECTS_ROOT_PATH, pathSrc)

def processFlatTopology(path, counter,pv, ftop):
    if ftop == None or len(ftop["topology"]) == 0:
        return False

    suffix = "_"+str(counter) #ftop["name"].split(".") + 
    logMsg = 'for parent '+path+" in kernel "+pv["name"]

    if len(ftop["args"]) != len(pv["args"]):
        raise Exception('len(ftop["args"]) != len(pv["args"]) '+logMsg)
    if len(ftop["emit"]) != len(pv["emit"]):
        raise Exception('len(kernel["emit"]) != len(parent["emit"]) '+logMsg)
    if len(ftop["receive"]) != len(pv["receive"]):
        raise Exception('len(kernel["receive"]) != len(parent["receive"]) '+logMsg)           
    
    renameChannels = dict()
    for i, e in enumerate(ftop["emit"]):
        if renameChannels.has_key(e["channel"]) and renameChannels[e["channel"]] != pv["emit"][i]["channel"]:
            raise Exception('renameChannels.has_key(e["channel"]) and renameChannels[e["channel"]] != pv["emit"][i]["channel"] '+logMsg)
        renameChannels[e["channel"]] = pv["emit"][i]["channel"]

    for i, e in enumerate(ftop["receive"]):
        if renameChannels.has_key(e["channel"]) and renameChannels[e["channel"]] != pv["receive"][i]["channel"]:
            raise Exception('renameChannels.has_key(e["channel"]) and renameChannels[e["channel"]] != pv["receive"][i]["channel"] '+logMsg)
        renameChannels[e["channel"]] = pv["receive"][i]["channel"]

    internalPropsNames = []
    for prop in ftop["props"]:
        if prop["name"] in internalPropsNames:
            raise Exception("in subtopology "+ftop["name"]+" there are two props with the same name "+prop["name"])
        internalPropsNames.append(prop["name"])
        prop["name"]+=suffix #rename prop with addition of suffix
        if prop["size"] != None and isinstance( prop["size"] , basestring ):
            prop["size"]+=suffix

    renameArgs = dict()
    for i, e in enumerate(ftop["args"]):
        if renameArgs.has_key(e["name"]) and renameArgs[e["name"]] != pv["args"][i]["value"]:
            raise Exception('renameArgs.has_key(e["name"]) and renameArgs[e["name"]] != pv["args"][i]["value"] '+logMsg)
        renameArgs[e["name"]] = pv["args"][i]["value"]

    internalChannelsNames = []
    for c in ftop["channels"]:
        if c["channel"] in internalChannelsNames:
            raise Exception("in subtopology "+ftop["name"]+" there are two channels with the same name "+c["channel"])
        internalChannelsNames.append(c["channel"])
        c["channel"] += suffix #rename channel with addition of suffix
        for e in c["args"]:
            if str(e["value"])[0].isdigit():
                continue
            if renameArgs.has_key(e["value"]):
                e["value"] = renameArgs[e["value"]] #rename arg to the parent arg name
            elif e["value"] in internalPropsNames:
                e["value"] += suffix #rename arg with addition of suffix
            else:
                raise Exception("in subtopology "+ftop["name"]+" channel '"+c["channel"]+"' the arg '"+e["value"]+"' is used but not defined neither in args nor props")

    for t in ftop["topology"]:
        t["parents"]=[ftop["name"]]+t["parents"]
        #RENAME FLATTEN TOPOLOGY CHANNEL NAMES
        for e in t["emit"]+t["receive"]:
            if renameChannels.has_key(e["channel"]):
                e["channel"] = renameChannels[e["channel"]] #rename channel to the parent channel name
            elif e["channel"] in internalChannelsNames:
                e["channel"] += suffix #rename channel with addition of suffix
            else:
                raise Exception("in subtopology "+ftop["name"]+" the channel '"+e["channel"]+"' is used but not defined neither in emit/receive nor channels")
        #RENAME FLATTEN TOPOLOGY ARGUMENTS NAMES
        for e in t["args"]:
            if str(e["value"])[0].isdigit():
                continue
            if renameArgs.has_key(e["value"]):
                e["value"] = renameArgs[e["value"]] #rename arg to the parent arg name
            elif e["value"] in internalPropsNames:
                e["value"] += suffix #rename arg with addition of suffix
            else:
                raise Exception("in subtopology "+ftop["name"]+" the arg '"+e["value"]+"' is used but not defined neither in args nor props")
        #RENAME PARALLEL ARGUMENT
        if not str(t["parallel"])[0].isdigit():
            if renameArgs.has_key(t["parallel"]):
                t["parallel"] = renameArgs[t["parallel"]] #rename arg to the parent arg name
            elif t["parallel"] in internalPropsNames:
                t["parallel"] += suffix #rename arg with addition of suffix
            else:
                raise Exception("in subtopology "+ftop["name"]+" the parallel argument '"+t["parallel"]+"' is used but not defined neither in args nor props")

    return True

def generateFlatTopology(visitedPaths, topology_dir):
    gernetFileName = os.path.join(topology_dir,"gernet")
    read_data = readGernet(gernetFileName)
    if read_data == None:
        raise Exception("files "+gernetFileName+".json/.yaml are not found")

    if len(read_data["topology"])==0 or (read_data["hide"] and len(visitedPaths)>0):
        if len(read_data["topology"])>0:
            read_data["topology"] = []
        return read_data

    visitedPaths += [read_data["name"]]
    sub_topologies = dict()
    for counter, pv in enumerate(read_data["topology"]):
        # run through the topology elements, detect cycles
        if pv["name"] in visitedPaths:
            raise Exception("Ring dependency detected: "+pv["name"]+" is included at least twice! Last inclusion from "+read_data["name"])

        ftop = generateFlatTopology(visitedPaths, getPath(pv["name"]))
        
        if processFlatTopology(read_data["name"],counter,pv,ftop):
            sub_topologies[counter] = ftop
            read_data["topology"][counter] = "None"

    #remove None elements from the topology
    read_data["topology"] =  [v for v in read_data["topology"] if v != "None"]

    for k, t in sub_topologies.iteritems():
        if t == None:
            continue
        for kernel in t["topology"]:
            #INJECT FLATTEN TOPOLOGY ELEMENT INTO THE PARENT TOPOLOGY
            read_data["topology"].append(kernel)
        for channel in t["channels"]:
            #INJECT FLATTEN TOPOLOGY CHANNEL INTO THE PARENT CHANNELS
            read_data["channels"].append(channel)
        for prop in t["props"]:
            read_data["props"].append(prop)

    return read_data

def verifyChannelsParameters(read_data):
    return # SIZE AND TIMEOUT COULD NOT BE SET BECAUSE OF USE OF THE OLD API
    isHidden = read_data['hide']
    for t in read_data["topology"]:
        for e in t["emit"]:
            # print e['channel']+" "+str(e['size'])
            if e['size'] == None or e['timeout'] == None:
                found = False
                searchList = read_data["channels"] if isHidden else read_data["emit"]+read_data["receive"]+read_data["channels"]
                for s in searchList:
                    # print s
                    if s['channel'] == e['channel'] and s['size'] != None and s['timeout'] != None and s['type'] != None:
                        found = True
                        # print "found"
                        break
                if not found:
                    if isHidden:
                        raise Exception(read_data["name"]+" : channels do not have "+e['channel']+" or size/timeout was not set")
                    else:
                        raise Exception(read_data["name"]+" : channels,emit,receive do not have "+e['channel']+" or size/timeout was not set")

def splitAndCheck(v, length):
    v = v.replace("  "," ")
    s = v.split(" ")
    if len(s) < length:
      raise Exception("splitAndCheck: len(s) < "+str(length)+" in "+v)
    return s

def parseEmitRecv(v):
    if not isinstance(v, basestring):
        return v
    s = splitAndCheck(v,1)
    typeS = s[1] if len(s) > 1 else None
    size = s[2] if len(s) > 2 else None
    timeout = s[3] if len(s) > 3 else None

    return {'channel':s[0],'type':typeS,'size':size, 'timeout': timeout}


def parseEmitRecvChannels(read_data, v):
    if not isinstance(v, basestring):
        return v
    s = splitAndCheck(v,1)
    v = dict()
    v["channel"] = s[0]
    v["type"] = s[1] if len(s) > 1 else None
    v["size"] = s[2] if len(s) > 2 else None
    v["timeout"] = s[3] if len(s) > 3 else None
    v["name"] = DefaultMapBuffer

    readers = 0

    for e in read_data["emit"]:
        if e["channel"] == v["channel"]:
            readers += 1

    for t in read_data["topology"]:
        for e in t["receive"]:
            if e["channel"] == v["channel"]:
                readers += 1
    if readers == 0:
        raise Exception("There is 0 readers for the declared "+v["channel"]+" channel")
    v["args"] = [{'value':readers}]
    if len(s) > 2:
        for arg in s[2:]:
            v["args"].append({'value':arg})
    
    return v

def parseProp(v):
    if not isinstance(v, basestring):
        if not v.has_key("value"):
            v["value"] = None
        if not v.has_key("size"):
            v["size"] = None
        return v
    s = splitAndCheck(v,2)

    size = None
    if "[" in s[1]:
        ts = s[1].split('[')
        s[1] = ts[0]+"[]"
        tmp = ts[1][:-1] #omit last character because it should be ']'
        try:
            size = int(tmp)
        except:
            size = tmp 

    value = s[2] if len(s) > 2 else None

    return {'name':s[0], 'type':s[1], 'size': size, 'value': value}

def parseArg(v, isInTopology):
    if not isinstance(v, basestring):
        return v

    s = splitAndCheck(v,1)

    t = s[1] if len(s)>1 else None
    name = 'value' if isInTopology else 'name'
    
    return {name+'' : s[0], 'type': t}

def filterTypes_java(t):
    serializableType = False
    isObject = True
    isArray = False
    if len(t)>2 and t[-2:] == '[]':
        isArray = True
        t = t[:-2]
    if t in ["string","String"]:
        t = "String"
        serializableType = True
    if t in ["byte"]:
        t = "byte" if isArray else "byte"
        isObject = False
        serializableType = True
    if t in ["char"]:
        t = "char" if isArray else "char"
        isObject = False
        serializableType = True
    if t in ["int"]:
        t = "int" if isArray else "int"
        isObject = False
        serializableType = True
    if t in ["unsigned","long"]:
        t = "long" if isArray else "long"
        isObject = False
        serializableType = True
    if t in ["boolean"]:
        t = "boolean" if isArray else "boolean"
        isObject = False
        serializableType = True
    if t in ["double"]:
        t = "double" if isArray else "double"
        isObject = False
        serializableType = True
    if t in ["float"]:
        t = "float" if isArray else "float"
        isObject = False
        serializableType = True
    if t in ["Object"]:
        t = "Object"
    if isArray:
        t += "[]"
        isObject = True
    return t, isObject, isArray, serializableType

def filterTypes_c(t):
    serializableType = False
    isObject = True
    isArray = False
    if len(t)>2 and t[-2:] == '[]':
        isArray = True
        t = t[:-2]
    if t in ["string","char*"]:
        t = "char*"
        serializableType = True
    if t in ["char"]:
        t = "char"
        isObject = False
        serializableType = True
    if t in ["int"]:
        t = "int32_t"
        isObject = False
        serializableType = True
    if t in ["unsigned"]:
        t = "uint32_t"
        isObject = False
        serializableType = True
    if t  in ["long"]:
        t = "int64_t"
        isObject = False
        serializableType = True
    if t in ["boolean"]:
        t = "BOOL" if isArray else "BOOL"
        isObject = False
        serializableType = True
    if t in ["double"]:
        t = "double"
        isObject = False
        serializableType = True
    if t in ["float"]:
        t = "float"
        isObject = False
        serializableType = True
    if t in ["Object"]:
        t = "void*"
    if isArray:
        t = "arrayObject"
        isObject = True
    return t, isObject, isArray, serializableType

def splitClassPath(classPath):
    classPath = classPath.split(" ")[0]
    classPathList = classPath.split('/')
    domainSplit = classPathList[0].split('.')
    if len(domainSplit)>1:
        domainPrefix = [domainSplit[1], domainSplit[0]]
    else:
        domainPrefix = [domainSplit[0]]
    del classPathList[0]
    classPathList = domainPrefix+classPathList
    return classPathList

def getClassName(path):
    fullNameList = splitClassPath(path)
    return fullNameList[-1].replace("-","_")

def getCompany(path):
    fullNameList = splitClassPath(path)
    return fullNameList[1]

def getCompanyDomain(path):
    fullNameList = splitClassPath(path)
    return fullNameList[1]+'.'+fullNameList[0]

def getDomainName(path):
    fullNameList = splitClassPath(path)
    del fullNameList[-1]
    return '.'.join(fullNameList)

def getDomainPath(path):
    fullNameList = splitClassPath(path)
    to_delete = [0,1]
    for offset, index in enumerate(to_delete):
        index -= offset
        del fullNameList[index]
    return getCompanyDomain(path)+'/'+('/'.join(fullNameList))

def getFullName(path):
    return '.'.join(splitClassPath(path))

def getFullName_(path):
    return '_'.join(reversed(splitClassPath(path))).replace("-","_")

def getRootPath(path):
    countstepsup = len(splitClassPath(path)) -3
    if countstepsup < 0:
        countstepsup = 0
    countstepsup += 2

    rd = []
    for v in range(0, countstepsup):
        rd.append("..")
    rd = os.path.join(*rd)
    return rd

def recurseDependencies(dependenciesDict):
  newDependenciesDict = dict()
  hasNewData = False
  for k,d in dependenciesDict.items():
    fileToRead = os.path.join( getPath(d["name"]), 'gernet' )
    # print "===> recurseDependencies: "+fileToRead
    read_data = readGernet(fileToRead)
    if read_data == None:
      # print "No Read Data"
      continue
    d["_depends"] = read_data["topology"]+read_data["depends"]
    for v in read_data["topology"]+read_data["depends"]:
      if not dependenciesDict.has_key(v["name"]) and not newDependenciesDict.has_key(v["name"]):
        # print v["name"]+" not in dependenciesDict and not in newDependenciesDict"
        newDependenciesDict[v["name"]] = v
        hasNewData = True
  if hasNewData:
    newDependenciesDict = recurseDependencies(newDependenciesDict)
    i = len(dependenciesDict)
    for k,v in newDependenciesDict.items():
      if not dependenciesDict.has_key(v["name"]):
        dependenciesDict[v["name"]] = v
        dependenciesDict[v["name"]]['_order'] = i
        i = i + 1
  return dependenciesDict

def getDependenciesDict(read_data):
  dependenciesDict = dict()

  i = len(dependenciesDict)
  for v in read_data["topology"]+read_data["depends"]:
    if not dependenciesDict.has_key(v["name"]):
      dependenciesDict[v["name"]] = v
      dependenciesDict[v["name"]]['_order'] = i
      i = i + 1

  dependenciesDict = recurseDependencies(dependenciesDict)

  #sorting
  dictToSort = dict()
  for k,v in dependenciesDict.items():
    dictToSort[v["_order"]] = v
  
  srt = sorted(dictToSort.items(), key=operator.itemgetter(0))

  dependenciesList = []
  for k, v in srt:
    minIndexToInsert = len(dependenciesList)
    for d in v["_depends"]: #foreach dependency
        #if there is interdependency within our project
        # if dependenciesDict.has_key(d["name"]):
        indxInList = -1
        for i, dl in enumerate(dependenciesList):
            if dl["name"] == d["name"]:
                indxInList = i
                break
        if indxInList >= 0 and indxInList < minIndexToInsert:
            minIndexToInsert = indxInList
    dependenciesList.insert(minIndexToInsert, v)
  return dependenciesList