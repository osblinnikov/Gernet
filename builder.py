import os.path
import os

import os, sys, inspect
# realpath() with make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
  sys.path.insert(0, cmd_folder)

# use this if you want to include modules from a subforder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"tools/cogapp")))
if cmd_subfolder not in sys.path:
  sys.path.insert(0, cmd_subfolder)

from cogapp import Cog
import json
from pprint import pprint
from shutil import copyfile

import os, sys, inspect
# realpath() with make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
  sys.path.insert(0, cmd_folder)

# use this if you want to include modules from a subforder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"tools/Mako")))
if cmd_subfolder not in sys.path:
  sys.path.insert(0, cmd_subfolder)

from mako.template import Template
from mako.lookup import TemplateLookup
from attrs import attrs

_Types = ['c','java']
generators = ['build','include','src','test','run']

def tpl(strfile, args):
  strfile = os.path.abspath(os.path.join(os.getcwd(),strfile))
  mylookup = TemplateLookup(directories=[
    os.path.abspath(os.getcwd())
  ])
  tplFromFile = Template(filename=strfile, lookup=mylookup, imports=['from attrs import attrs'])
  return tplFromFile.render(a=args)

join = os.path.join
#PLEASE change it if you don't want the standard gernets location
PROJECTS_ROOT_PATH = os.path.abspath(join(os.path.dirname(__file__),'..','..','..','..','..','..'))

def getOutputFile_c(generator, TopologyDir, fullName):
    fullNameList = fullName.split('.')
    className = fullNameList[-1]
    outputFile=None
    if generator=='build':
        outputFile = join(checkDir(join(TopologyDir,'c')),'SNocscript.py')
    elif generator=='include':
        outputFile = join(checkDir(join(TopologyDir,'c','include')),className+".h")
    elif generator=='test':
        outputFile = join(checkDir(join(TopologyDir,'c','tests')),className+"Test.c")
    elif generator=='src':
        outputFile = join(checkDir(join(TopologyDir,'c','src')),className+".c")
    elif generator=='run':
        outputFile = join(checkDir(join(TopologyDir,'c','src')),"main.c")
    else:
        print "getOutputFile_c: unknown generator "+generator+" for `c` language"
        exit()
    return outputFile

def getOutputFile_java(generator, TopologyDir, fullName):
    fullNameList = fullName.split('.')
    className = fullNameList[-1]
    # del fullNameList[-1]
    outputFile=None
    if generator=='build':
        outputFile = join(checkDir(join(TopologyDir,'java')),'pom.xml')
    elif generator=='include':
        log = "include is not required for java"
        # print log
    elif generator=='test':
        outputFile = join(checkDir(join(*[TopologyDir,'java','src','test','java']+fullNameList)),className+'Test.java')
    elif generator=='src':
        outputFile = join(checkDir(join(*[TopologyDir,'java','src','main','java']+fullNameList)),className+'.java')
    elif generator=='run':
        outputFile = join(checkDir(join(*[TopologyDir,'java','src','main','java']+fullNameList)),'main.java')
    else:
        print "getOutputFile_java: unknown generator "+generator+" for `java` language"
        exit()
    return outputFile

def runCog(firstRealArgI, argv, TopologyDir):
    Types = _Types
    OTHER_ARGUMENTS = []
    CLEANING_STAGE = 0
    if len(argv) > firstRealArgI + 1:
        for i in range(firstRealArgI + 1, len(argv)):
            if argv[i] == '-h':
                printHelp()
                exit()
            elif argv[i] == '-c':
                CLEANING_STAGE = 1
            elif argv[i] == '-lang':
                if i + 1 == len(argv) or argv[i+1].startswith("-"):
                    print "expected language type {c,java} after -lang option"
                    exit()
                else:
                    Types = [argv[i+1]]
                    i = i + 1
            elif argv[i-1] == '-lang' or i == 1:
                continue
            else:
                OTHER_ARGUMENTS.push(argv[i])

    cleaning_arg = ['-U','-c'] #-u means unix style line endings
    if CLEANING_STAGE != 0:
      cleaning_arg = ['-x']

    jsonFileToRead = join(TopologyDir,"gernet.json")
    json_data=open(jsonFileToRead)
    read_data = json.load(json_data)
    json_data.close()
    # pprint(read_data)
    typeOfBlock = "kernel"
    if read_data.has_key("type"):
        typeOfBlock = read_data["type"]
    fullName = read_data["path"]
    if fullName == None:
        print "path is not specified in gernet.json"
        exit()
    

    curPath = os.path.abspath(os.path.dirname(__file__))
    for i in range(0, len(Types)):
        for generator in generators:
            outputFile = None
            if Types[i] == 'c':
                outputFile = getOutputFile_c(generator, TopologyDir, fullName)
            elif Types[i] == 'java':
                outputFile = getOutputFile_java(generator, TopologyDir, fullName)
            else:
                print "runCog: unknown language type "+Types[i]
                exit()
            if outputFile == None:
                continue
            #process template file and write output into .java/.c files
            if not os.path.isfile(outputFile):
                f = open(outputFile,'w')#output file
                f.write(tpl(
                    join(curPath,Types[i],generator,typeOfBlock),#input template
                    attrs(
                        prefix=jsonFileToRead,#required for parser of json file
                        parserPath=join(curPath,Types[i])
                    )#args
                ))
                f.close() 

            #process final .java, .c files with use of template going along the file
            argv = ['cogging']+OTHER_ARGUMENTS+cleaning_arg+[
                '-I',
                curPath, 
                '-I',
                join(curPath,Types[i]),
                '-r',#replace in file
                "-D","configFile="+jsonFileToRead, #specify config as global variable
                "-D","templateFile="+join(curPath,Types[i],generator,typeOfBlock+'.tpl'), #specify config as global variable
                outputFile
            ]
            # print argv
            ret = Cog().main(argv)
def checkDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def printHelp():
    print "**********************"
    print "Gents is a little wrapper on Cogapp (http://nedbatchelder.com/code/cog)."
    print "which enables you to generate full implementations of cnets/jnets topologies"
    print "Usage: gernet [TopologyFilePath] [options]"
    print "Examples:"
    print "  gernet .. -lang java" 
    print "  gernet icanchangethisdomain/SomeProjectName  #generate with every available generator"
    print "TopologyFilePath can be absolute, relative to current path, or "
    print "relative to projects root path e.g.:"
    print "  gernet github.com\\airutech\\gernet\\example -lang java"
    print "**********************"
    print "Available options:"
    print "  -lang {C,java}"
    print "  -h        # print this help"
    print "  -c        # execute cleaning only for chosen Topology"
    print "**********************"
    print "Other options can be Cog specific."
    print "  If you want to change default path to the Projects directory please see the"
    print "  builder.py file and PROJECTS_ROOT_PATH variable"
    print "**********************"
