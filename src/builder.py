# realpath() with make your script run, even if you symlink it :)
#
# cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
# if cmd_folder not in sys.path:
# sys.path.insert(0, cmd_folder)
#
# use this if you want to include modules from a subforder
import inspect
import re
import subprocess
import sys
from attrs import attrs
import json, os

sysPathBcp = list(sys.path+[os.path.dirname(__file__)])

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0])))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from gernetHelpers import *
from cogapp import cogapp
import mako.template
import mako.lookup

join = os.path.join


def tpl(strfile, args):
    mylookup = mako.lookup.TemplateLookup(directories=[
        os.path.abspath(os.getcwd())
    ])
    tplFromFile = mako.template.Template(filename=strfile, lookup=mylookup, imports=['from src.attrs import attrs'])
    return tplFromFile.render(a=args)


def getArgs(firstRealArgI, argv, Types):
    all_args = []
    compiling_arg = ['-U', '-c']  #-U means unix style line endings

    if len(argv) > firstRealArgI + 1:
        for i in range(firstRealArgI + 1, len(argv)):
            if argv[i] == '-c':
                compiling_arg = ['-x']
            elif argv[i] == '-g':
                if i + 1 == len(argv) or argv[i + 1].startswith("-"):
                    raise Exception("expected language type after -lang option")
                else:
                    Types.append(argv[i + 1])
                    i = i + 1
            elif argv[i - 1] == '-g' or i == 1:
                continue
            else:
                all_args.append(argv[i])
    all_args += compiling_arg
    return all_args


def getFilteredSubFolders(folder, filters):
    res = []
    d = []
    for root, dirs, files in os.walk(folder):
        d = dirs
        break

    for i in d:
        if len(filters) == 0 or i in filters:
            res.append(i)
    return res

def getPath(pathSrc):
    path = pathSrc.split('.')
    if len(path) < 3:
        raise Exception("path: \""+pathSrc+"\" is not a full package name")
    arr = [PROJECTS_ROOT_PATH, path[1] + "." + path[0]]
    to_delete = [0, 1]
    for offset, index in enumerate(to_delete):
        index -= offset
        del path[index]
    return '/'.join(arr + path)


def generateMissedFiles(topology_dir, generator_dir, classPath, extra_args):
    classPathList = classPath.split('.')
    fullName_ = '_'.join(classPathList)
    className = classPathList[-1]
    json_file_to_read = join(topology_dir, "gernet.json")
    for root, dirs, files in os.walk(generator_dir):
        for fileName in files:
            file = os.path.join(root,fileName)
            if (len(fileName)>4 and fileName[-4:] == '.tpl') or not os.path.exists(file+".tpl"):
                continue

            generator_dirLen = (len(generator_dir))+1
            relativeFilePath =  file[generator_dirLen:]\
                .replace("_NAME_", className) \
                .replace("_FULLNAME_", fullName_) \
                .replace("_FULLNAMEDIR_", os.path.join(*[fullName_, ""])) \
                .replace("_PATH_", os.path.join(*(classPathList+[""])))\
                .replace("_GERNET_","gernet")
            absDstFilePath = os.path.join(topology_dir, os.path.split(generator_dir)[1], relativeFilePath)
            if not os.path.exists(absDstFilePath):
                checkDir(absDstFilePath)

                #cleaning paths before copying template
                sys.path = list(sysPathBcp)

                f = open(absDstFilePath,'w')#output file
                f.write(tpl(
                    file,#input template
                    attrs(
                        prefix=json_file_to_read,#required for parser of json file
                        parserPath=generator_dir
                    )#args
                ))
                f.close()

            #cleaning paths before cogging template
            sys.path = list(sysPathBcp)
            args = extra_args+[
                '-I',
                os.path.abspath(os.path.dirname(__file__)),
                '-I',
                generator_dir,
                '-r',#replace in file
                "-D","configFile="+json_file_to_read, #specify config as global variable
                "-D","templateFile="+file+'.tpl', #specify config as global variable
                absDstFilePath
            ]
            # print args
            cogapp.Cog().main(["cogging"]+args)

def processFlatTopology(path, counter,pv, ftop):
    if ftop == None or len(ftop["topology"]) == 0:
        return False

    suffix = "_".join( [] + [str(counter)] ) #ftop["path"].split(".") + 
    logMsg = 'for parent '+path+" in kernel "+pv["path"]

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
            raise Exception("in subtopology "+ftop["path"]+" there are two props with the same name "+prop["name"])
        internalPropsNames.append(prop["name"])
        prop["name"]+=suffix #rename prop with addition of suffix

    renameArgs = dict()
    for i, e in enumerate(ftop["args"]):
        if renameArgs.has_key(e["name"]) and renameArgs[e["name"]] != pv["args"][i]["value"]:
            raise Exception('renameArgs.has_key(e["name"]) and renameArgs[e["name"]] != pv["args"][i]["value"] '+logMsg)
        renameArgs[e["name"]] = pv["args"][i]["value"]

    internalChannelsNames = []
    for c in ftop["channels"]:
        if c["channel"] in internalChannelsNames:
            raise Exception("in subtopology "+ftop["path"]+" there are two channels with the same name "+c["channel"])
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
                raise Exception("in subtopology "+ftop["path"]+" channel '"+c["channel"]+"' the arg '"+e["value"]+"' is used but not defined neither in args nor props")

    for t in ftop["topology"]:
        t["parents"]=[ftop["path"]]+t["parents"]
        #RENAME FLATTEN TOPOLOGY CHANNEL NAMES
        for e in t["emit"]+t["receive"]:
            if renameChannels.has_key(e["channel"]):
                e["channel"] = renameChannels[e["channel"]] #rename channel to the parent channel name
            elif e["channel"] in internalChannelsNames:
                e["channel"] += suffix #rename channel with addition of suffix
            else:
                raise Exception("in subtopology "+ftop["path"]+" the channel '"+e["channel"]+"' is used but not defined neither in emit/receive nor channels")
        #RENAME FLATTEN TOPOLOGY ARGUMENTS NAMES
        for e in t["args"]:
            if str(e["value"])[0].isdigit():
                continue
            if renameArgs.has_key(e["value"]):
                e["value"] = renameArgs[e["value"]] #rename arg to the parent arg name
            elif e["value"] in internalPropsNames:
                e["value"] += suffix #rename arg with addition of suffix
            else:
                raise Exception("in subtopology "+ftop["path"]+" the arg '"+e["value"]+"' is used but not defined neither in args nor props")
        #RENAME PARALLEL ARGUMENT
        if not str(t["parallel"])[0].isdigit():
            if renameArgs.has_key(t["parallel"]):
                t["parallel"] = renameArgs[t["parallel"]] #rename arg to the parent arg name
            elif t["parallel"] in internalPropsNames:
                t["parallel"] += suffix #rename arg with addition of suffix
            else:
                raise Exception("in subtopology "+ftop["path"]+" the parallel argument '"+t["parallel"]+"' is used but not defined neither in args nor props")

    return True
    

def generateFlatTopology(visitedPaths, topology_dir):
    gernetFileName = join(topology_dir,"gernet")
    read_data = readGernet(gernetFileName)
    if read_data == None:
        raise Exception("files "+gernetFileName+".json/.yaml are not found")

    if len(read_data["topology"])==0 or read_data["hide"]:
        if len(read_data["topology"])>0:
            read_data["topology"] = []
        return read_data

    visitedPaths += [read_data["path"]]
    sub_topologies = dict()
    for counter, pv in enumerate(read_data["topology"]):
        # run through the topology elements, detect cycles
        if pv["path"] in visitedPaths:
            raise Exception("Ring dependency detected: "+pv["path"]+" is included at least twice! Last inclusion from "+read_data["path"])

        ftop = generateFlatTopology(visitedPaths, getPath(pv["path"]))
        
        if processFlatTopology(read_data["path"],counter,pv,ftop):
            sub_topologies[counter] = ftop
            read_data["topology"][counter] = "None"

    #remove None elements from the topology
    read_data["topology"] =  [value for value in read_data["topology"] if value != "None"]

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


def runGernet(firstRealArgI, argv, topology_dir):
    Types = []
    extra_args = getArgs(firstRealArgI, argv, Types)

    read_data = generateFlatTopology([],topology_dir)

    print json.dumps(read_data, indent=4, sort_keys=True)

    return

    for p in read_data["gen"]:
        p0 = getPath(p)
        Types = getFilteredSubFolders(p0, Types)
        # if len(Types) == 0:
            # print ("No one generator was found")
            # return
        for i in range(0, len(Types)):
            generateMissedFiles(
                topology_dir, #path to the directory with the topology
                os.path.join(p0, Types[i]),#generator_directory
                read_data["path"],#module full name
                extra_args # extra arguments for the Cog
            )


def checkDir(directory):
    fPath, fName = os.path.split(directory)
    if not os.path.exists(fPath):
        os.makedirs(fPath)
    return fPath
