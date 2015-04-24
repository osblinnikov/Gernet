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
import yaml

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

def generateMissedFiles(topology_dir, generator_dir, classPath, extra_args):
    fullName_ = getFullName_(classPath)
    className = getClassName(classPath)
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
                .replace("_PATH_", os.path.join(*(splitClassPath(classPath)+[""]))) \
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
def runGernet(firstRealArgI, argv, topology_dir):
    Types = []
    extra_args = getArgs(firstRealArgI, argv, Types)

    read_data = generateFlatTopology([],topology_dir)

    verifyChannelsParameters(read_data)

    outputfn = os.path.join(topology_dir,"flat.gernet.yaml")
    f = open(outputfn,"w")
    f.write(yaml.safe_dump(read_data, default_flow_style=False, indent=4))
    f.close()

    print " => created "+outputfn

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
                read_data["name"],#module full name
                extra_args # extra arguments for the Cog
            )


def checkDir(directory):
    fPath, fName = os.path.split(directory)
    if not os.path.exists(fPath):
        os.makedirs(fPath)
    return fPath
